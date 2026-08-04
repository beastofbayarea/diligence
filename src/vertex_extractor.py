"""
vertex_extractor.py — Vertex AI (Gemini) integration helper for model extraction

Usage:
- Requires google-cloud-aiplatform installed and GOOGLE_APPLICATION_CREDENTIALS pointing to a key.
- Environment variables: GCP_PROJECT_ID, GCP_REGION, GEMINI_MODEL

Behavior:
- Builds a compact prompt using src.prompts.build_prompt
- Calls Vertex AI PredictionServiceClient.predict on the configured model
- Expects the model to return JSON matching the response schema; parses and returns claims list

This is a best-effort implementation for CI/local use. If the environment is not configured
or the client import fails, the functions return None so the pipeline can fall back to the
heuristic extractor.
"""

import os
import json
import time


def extract_with_vertex(pdf_paths):
    # Check config
    project = os.environ.get('GCP_PROJECT_ID')
    region = os.environ.get('GCP_REGION', 'global')
    model = os.environ.get('GEMINI_MODEL')
    if not project or not model:
        print('Vertex extractor not configured (GCP_PROJECT_ID or GEMINI_MODEL missing).')
        return None
    try:
        from src import prompts
        prompt_text = prompts.build_prompt([])  # will be replaced with actual pages below
    except Exception:
        prompt_text = None
    # Read PDFs (avoid heavy memory usage) — reuse code from model_extractor's reader if available
    try:
        from pypdf import PdfReader
    except Exception as e:
        print('pypdf not installed; cannot assemble PDF payload for Vertex extractor')
        return None
    files_payload = []
    for pdf in pdf_paths:
        try:
            reader = PdfReader(pdf)
        except Exception as e:
            print(f'Could not read {pdf}: {e}')
            continue
        pages = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ''
            pages.append({'page': i, 'text': text})
        files_payload.append({'name': os.path.basename(pdf), 'path': pdf, 'pages': pages})
    # Build prompt
    try:
        from src import prompts
        prompt_text = prompts.build_prompt(files_payload)
    except Exception:
        prompt_text = json.dumps({'files': files_payload})[:1000]
    # Call Vertex AI prediction
    try:
        from google.cloud import aiplatform
        from google.cloud.aiplatform.gapic import PredictionServiceClient
        # Client will pick up GOOGLE_APPLICATION_CREDENTIALS from env
        client = PredictionServiceClient(client_options={"api_endpoint": f"{region}-aiplatform.googleapis.com"})
        # Model resource name: projects/{project}/locations/{region}/models/{model}
        model_name = f"projects/{project}/locations/{region}/models/{model}"
        instances = [{"content": prompt_text}]
        params = {}
        response = client.predict(endpoint=model_name, instances=instances, parameters=params)
        return response
    except Exception as e:
        print(f'Vertex extraction failed: {e}')
        return None


# helper to allow model_verifier to call Vertex with a prompt directly
def call_model_prompt(prompt_text):
    project = os.environ.get('GCP_PROJECT_ID')
    region = os.environ.get('GCP_REGION', 'global')
    model = os.environ.get('GEMINI_MODEL')
    if not project or not model:
        print('Vertex not configured for call_model_prompt')
        return None
    try:
        from google.cloud.aiplatform.gapic import PredictionServiceClient
        client = PredictionServiceClient(client_options={"api_endpoint": f"{region}-aiplatform.googleapis.com"})
        model_name = f"projects/{project}/locations/{region}/models/{model}"
        instances = [{"content": prompt_text}]
        response = client.predict(endpoint=model_name, instances=instances)
        return response
    except Exception as e:
        print(f'Vertex call_model_prompt failed: {e}')
        return None
        # Response parsing: try to pull prediction payload text
        predictions = []
        for p in response.predictions:
            # p may be a dict-like; try to find 'content' or 'output' fields
            if isinstance(p, dict):
                for k in ('content', 'output', 'text', 'response'):
                    if k in p and isinstance(p[k], str):
                        try:
                            js = json.loads(p[k])
                            if isinstance(js, list):
                                predictions = js
                                break
                        except Exception:
                            continue
        if not predictions:
            # try to interpret the whole response as text
            try:
                text_resp = str(response)
                # attempt to find JSON substring
                import re
                m = re.search(r'(\[\s*\{.*\}\s*\])', text_resp, re.S)
                if m:
                    predictions = json.loads(m.group(1))
            except Exception:
                pass
        out = []
        for c in predictions:
            if not isinstance(c, dict):
                continue
            if 'claim' in c and 'source_file' in c and 'page' in c:
                out.append({'claim': c['claim'], 'source_file': c['source_file'], 'page': int(c['page']), 'type': c.get('type','model')})
        return out
    except Exception as e:
        print(f'Vertex extraction failed: {e}')
        return None


if __name__ == '__main__':
    import sys
    paths = sys.argv[1:]
    res = extract_with_vertex(paths)
    if res is None:
        print('Vertex extractor not run or failed')
    else:
        print(f'Vertex extracted {len(res)} claims')
