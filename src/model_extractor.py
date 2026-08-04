"""
model_extractor.py — call an external model API (e.g., Gemini) to extract claims from multiple PDFs in one request.

Behavior:
- Reads PDFs and builds a compact JSON payload with filenames and page texts.
- If env MODEL_API_URL and GEMINI_API_KEY are set, POSTs the payload with a response schema request.
- Parses the response expecting a JSON array of claims with fields: claim, source_file, page, type.
- On failure or missing config, returns None so caller can fallback to heuristic extractor.

Notes: Set MODEL_API_URL and GEMINI_API_KEY in the environment before running the pipeline.
"""

import os
import json
import requests
from typing import List, Optional


def read_pdfs_to_payload(pdf_paths: List[str]):
    try:
        from pypdf import PdfReader
    except Exception:
        raise RuntimeError('pypdf not installed')
    files = []
    for pdf in pdf_paths:
        try:
            reader = PdfReader(pdf)
        except Exception:
            continue
        pages = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ''
            pages.append({'page': i, 'text': text})
        files.append({'name': os.path.basename(pdf), 'path': pdf, 'pages': pages})
    return files


def extract_with_model(pdf_paths: List[str]) -> Optional[List[dict]]:
    """Return list of claims or None on config/error."""
    model_url = os.environ.get('MODEL_API_URL')
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('MODEL_API_KEY')
    if not model_url or not api_key:
        print('Model extractor not configured (MODEL_API_URL or GEMINI_API_KEY missing).')
        return None
    files_payload = read_pdfs_to_payload(pdf_paths)
    if not files_payload:
        print('No PDF content to send to model')
        return []
    # Response schema: expect an array of objects with keys claim, source_file, page, type
    response_schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'claim': {'type': 'string'},
                'source_file': {'type': 'string'},
                'page': {'type': 'integer'},
                'type': {'type': 'string'}
            },
            'required': ['claim', 'source_file', 'page']
        }
    }
    # Use prompts helper if available to build a clear prompt
    try:
        from src import prompts
        prompt_text = prompts.build_prompt(files_payload)
        payload = {
            'files': files_payload,
            'response_schema': response_schema,
            'prompt': prompt_text
        }
    except Exception:
        payload = {
            'files': files_payload,
            'response_schema': response_schema,
            'instructions': 'Extract falsifiable claims from these PDFs. Return JSON matching response_schema.'
        }
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        resp = requests.post(model_url, headers=headers, data=json.dumps(payload), timeout=120)
        resp.raise_for_status()
        data = resp.json()
        # Model might return wrapped structure; try to find top-level array
        if isinstance(data, dict) and 'claims' in data:
            claims = data['claims']
        elif isinstance(data, list):
            claims = data
        else:
            # Attempt to parse a JSON string in 'content' or similar
            if isinstance(data, dict) and 'content' in data:
                try:
                    claims = json.loads(data['content'])
                except Exception:
                    print('Model response parsing failed')
                    return None
            else:
                print('Unexpected model response format')
                return None
        # Basic validation
        out = []
        for c in claims:
            if not isinstance(c, dict):
                continue
            if 'claim' in c and 'source_file' in c and 'page' in c:
                c.setdefault('type', 'model')
                out.append({'claim': c['claim'], 'source_file': c['source_file'], 'page': int(c['page']), 'type': c.get('type','model')})
        return out
    except Exception as e:
        print(f'Model extraction failed: {e}')
        return None


if __name__ == '__main__':
    import sys
    paths = sys.argv[1:]
    claims = extract_with_model(paths)
    if claims is None:
        print('No model extraction performed')
    else:
        print(f'Extracted {len(claims)} claims from model')
