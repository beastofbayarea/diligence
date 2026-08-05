"""
prompts.py — prompt templates and response-schema helpers for model extraction

Provides a template for requesting a strict JSON response from a model (e.g., Gemini).
Adjust MODEL_PROMPT_TEMPLATE if needed for different model providers.
"""

RESPONSE_SCHEMA = {
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

MODEL_PROMPT_TEMPLATE = (
    "You are a precise data-extraction assistant. Given the following documents (PDF pages), "
    "extract all falsifiable claims. For each claim, return a JSON object with keys: 'claim' (the sentence), "
    "'source_file' (the originating filename), 'page' (page number as integer), and 'type' (a short tag like 'financial', 'metric', 'assertion').\n\n"
    "Return ONLY a JSON array matching the provided response schema. Do NOT return any extra text or commentary. "
    "If uncertain about a claim, omit it. Prioritize accuracy and provenance." 
)


def build_prompt(files_payload):
    """Builds a compact prompt body summarizing files and pages for the model.
    files_payload is a list of {name, path, pages:[{page, text}]}
    """
    parts = ["Extract falsifiable claims from the following documents. Return a JSON array matching the schema exactly."]
    for f in files_payload:
        parts.append(f"FILE: {f.get('name')} — {len(f.get('pages',[]))} pages")
        for p in f.get('pages', []):
            text = p.get('text', '').strip()
            if text:
                parts.append(f"PAGE {p.get('page')}:\n{text}")
    parts.append('\nSchema: ' + str(RESPONSE_SCHEMA))
    parts.append('\nInstructions: ' + MODEL_PROMPT_TEMPLATE)
    return '\n\n'.join(parts)

