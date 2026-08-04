"""
model_verifier.py — ask a model to classify claims as verified/contradicted/unverifiable

Behavior:
- If Vertex configured, attempt a Vertex call; else if MODEL_API_URL configured, call HTTP endpoint.
- Payload: a prompt listing claims and asking for a JSON array of {claim, status, evidence}
- Returns a dict mapping claim text -> {status, evidence}
"""
import os
import json
import requests

RESPONSE_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'claim': {'type': 'string'},
            'status': {'type': 'string'},
            'evidence': {'type': 'string'}
        },
        'required': ['claim','status']
    }
}


def build_prompt_for_verification(claims):
    parts = ["For each claim, answer with status in {verified, contradicted, unverifiable} and a short evidence string (if available). Return ONLY a JSON array."]
    parts.append('Claims:')
    for c in claims:
        parts.append(f"- {c.get('claim')}")
    parts.append('\nSchema: ' + str(RESPONSE_SCHEMA))
    return '\n'.join(parts)


def verify_with_model(claims):
    # claims: list of dicts
    model_url = os.environ.get('MODEL_API_URL')
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('MODEL_API_KEY')
    project = os.environ.get('GCP_PROJECT_ID')
    gemini_model = os.environ.get('GEMINI_MODEL')
    prompt = build_prompt_for_verification(claims)
    # Try Vertex first
    if project and gemini_model:
        try:
            from src import vertex_extractor
            # Use vertex_extractor to call model with prompt as content
            res = vertex_extractor.call_model_prompt(prompt)
            return _parse_model_verification_response(res)
        except Exception:
            pass
    # Try HTTP model_url
    if not model_url or not api_key:
        return None
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'prompt': prompt, 'response_schema': RESPONSE_SCHEMA}
    try:
        resp = requests.post(model_url, headers=headers, data=json.dumps(payload), timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # parse
        if isinstance(data, list):
            parsed = data
        elif isinstance(data, dict) and 'claims' in data:
            parsed = data['claims']
        elif isinstance(data, dict) and 'content' in data:
            try:
                parsed = json.loads(data['content'])
            except Exception:
                return None
        else:
            return None
        return _parse_model_verification_response(parsed)
    except Exception as e:
        print(f'Model verification failed: {e}')
        return None


def _parse_model_verification_response(parsed):
    out = {}
    if not isinstance(parsed, list):
        return None
    for item in parsed:
        if not isinstance(item, dict):
            continue
        claim = item.get('claim')
        status = item.get('status')
        evidence = item.get('evidence','')
        if claim and status:
            out[claim] = {'status': status, 'evidence': evidence}
    return out


if __name__ == '__main__':
    import sys
    print('model_verifier module — not a standalone script')
