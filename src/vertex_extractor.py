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
    # First try the google.generativeai client if available (generative models)
    try:
        import google.generativeai as genai
        # Attempt to use application default credentials when no API key is provided
        try:
            genai.configure()
        except Exception:
            pass
        try:
            resp = genai.generate_text(model=model, prompt=prompt_text)
            return resp
        except Exception:
            try:
                resp = genai.generate(model=model, input=prompt_text)
                return resp
            except Exception:
                pass
    except Exception:
        pass

    # Next try REST call to Vertex AI predict endpoint using OAuth2 ADC token
    try:
        import google.auth
        from google.auth.transport.requests import Request as AuthRequest
        creds, gproject = google.auth.default()
        # refresh to obtain token
        auth_req = AuthRequest()
        creds.refresh(auth_req)
        token = creds.token
        import requests as _req
        # Try several model resource name variants
        candidates = []
        if model.startswith('projects/'):
            candidates.append(model)
        else:
            candidates.append(f"projects/{project}/locations/{region}/models/{model}")
            candidates.append(f"projects/{project}/locations/global/publishers/google/models/{model}")
            candidates.append(f"projects/{project}/locations/{region}/publishers/google/models/{model}")
        # Build endpoint URL and try
        for model_name in candidates:
            # model_name may be full resource or path; strip leading 'projects/' if present when building URL
            try:
                # extract the model id path after 'projects/' to form URL
                if model_name.startswith('projects/'):
                    url = f"https://{region}-aiplatform.googleapis.com/v1/{model_name}:predict"
                else:
                    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project}/locations/{region}/models/{model}:predict"
                headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
                body = {'instances': [{ 'content': prompt_text }], 'parameters': {}}
                r = _req.post(url, headers=headers, json=body, timeout=120)
                if r.status_code == 200:
                    try:
                        return r.json()
                    except Exception:
                        return r.text
                else:
                    # continue to next candidate
                    continue
            except Exception:
                continue
    except Exception:
        pass

    # Next try the high-level aiplatform.Model.predict API
    try:
        from google.cloud import aiplatform
        aiplatform.init(project=project, location=region)
        # Determine model resource name variants to try
        candidates = []
        if model.startswith('projects/'):
            candidates.append(model)
        else:
            candidates.append(f"projects/{project}/locations/{region}/models/{model}")
            candidates.append(f"projects/{project}/locations/global/publishers/google/models/{model}")
            candidates.append(f"projects/{project}/locations/{region}/publishers/google/models/{model}")
        for cand in candidates:
            try:
                m = aiplatform.Model(cand)
                resp = m.predict(instances=[{"content": prompt_text}])
                return resp
            except Exception:
                continue
    except Exception:
        pass
    # Fallback to PredictionServiceClient with multiple endpoint/model resource attempts
    try:
        from google.cloud.aiplatform.gapic import PredictionServiceClient
        # Try a few api endpoints commonly used
        endpoints = [f"{region}-aiplatform.googleapis.com", f"{region}-aiplatform.googleapis.com:443", 'us-central1-aiplatform.googleapis.com']
        model_candidates = []
        if model.startswith('projects/'):
            model_candidates.append(model)
        else:
            model_candidates.append(f"projects/{project}/locations/{region}/models/{model}")
            model_candidates.append(f"projects/{project}/locations/global/publishers/google/models/{model}")
            model_candidates.append(f"projects/{project}/locations/{region}/publishers/google/models/{model}")
        for ep in endpoints:
            try:
                client = PredictionServiceClient(client_options={"api_endpoint": ep})
            except Exception:
                continue
            instances = [{"content": prompt_text}]
            params = {}
            for model_name in model_candidates:
                try:
                    resp = client.predict(endpoint=model_name, instances=instances, parameters=params)
                    return resp
                except Exception:
                    continue
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
    # Try high-level aiplatform.Model.predict first
    try:
        from google.cloud import aiplatform
        aiplatform.init(project=project, location=region)
        candidates = []
        if model.startswith('projects/'):
            candidates.append(model)
        else:
            candidates.append(f"projects/{project}/locations/{region}/models/{model}")
            candidates.append(f"projects/{project}/locations/global/publishers/google/models/{model}")
            candidates.append(f"projects/{project}/locations/{region}/publishers/google/models/{model}")
        for cand in candidates:
            try:
                m = aiplatform.Model(cand)
                resp = m.predict(instances=[{"content": prompt_text}])
                return resp
            except Exception:
                continue
    except Exception:
        pass
    # Fallback to PredictionServiceClient
    try:
        from google.cloud.aiplatform.gapic import PredictionServiceClient
        endpoints = [f"{region}-aiplatform.googleapis.com", f"{region}-aiplatform.googleapis.com:443", 'us-central1-aiplatform.googleapis.com']
        model_candidates = []
        if model.startswith('projects/'):
            model_candidates.append(model)
        else:
            model_candidates.append(f"projects/{project}/locations/{region}/models/{model}")
            model_candidates.append(f"projects/{project}/locations/global/publishers/google/models/{model}")
            model_candidates.append(f"projects/{project}/locations/{region}/publishers/google/models/{model}")
        for ep in endpoints:
            try:
                client = PredictionServiceClient(client_options={"api_endpoint": ep})
            except Exception:
                continue
            instances = [{"content": prompt_text}]
            for model_name in model_candidates:
                try:
                    resp = client.predict(endpoint=model_name, instances=instances)
                    return _parse_vertex_response(resp)
                except Exception:
                    continue
    except Exception as e:
        print(f'Vertex call_model_prompt failed: {e}')
    return None


def _parse_vertex_response(response):
    if response is None:
        return None
    if isinstance(response, list):
        return response
    predictions = []
    if hasattr(response, 'predictions'):
        for p in response.predictions:
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
        try:
            text_resp = str(response)
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
            out.append({'claim': c['claim'], 'source_file': c['source_file'], 'page': int(c['page']), 'type': c.get('type', 'model')})
    return out if out else None


if __name__ == '__main__':
    import sys
    paths = sys.argv[1:]
    res = extract_with_vertex(paths)
    if res is None:
        print('Vertex extractor not run or failed')
    else:
        print(f'Vertex extracted {len(res)} claims')

