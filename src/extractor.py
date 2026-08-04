"""
extractor.py — simple claim extraction using pypdf and heuristics

- extract(pdf_paths) -> list of claims (dicts with claim, source_file, page, type)
- write_claims(claims, out_path)

This is a pragmatic extractor for prototype/demo: it extracts text per page,
breaks into sentences, and heuristically selects sentences that look like
quantitative or business claims (numbers, %s, keywords).
"""

import json
import re


KEYWORDS = [
    'revenue', 'users', 'growth', 'funded', 'raised', 'annual', 'monthly',
    'mrr', 'arr', 'customers', 'growth', 'valuation', 'funding', 'profit', 'loss'
]


def extract(pdf_paths):
    claims = []
    if not pdf_paths:
        return claims
    # try to import pypdf
    try:
        from pypdf import PdfReader
    except Exception:
        print('pypdf not installed. Install with: pip install pypdf')
        return claims
    for pdf in pdf_paths:
        try:
            reader = PdfReader(pdf)
        except Exception as e:
            print(f'Could not read {pdf}: {e}')
            continue
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ''
            # split into sentences (simple)
            sentences = re.split(r'(?<=[.!?])\s+', text)
            for s in sentences:
                s_clean = ' '.join(s.split()).strip()
                if len(s_clean) < 40:
                    continue
                if looks_like_claim(s_clean):
                    claims.append({
                        'claim': s_clean,
                        'source_file': pdf.replace('\\', '/'),
                        'page': i,
                        'type': 'heuristic'
                    })
    return claims


def looks_like_claim(s):
    # contains a number or percentage and a keyword OR long numeric claim
    if re.search(r'\d', s) and any(k in s.lower() for k in KEYWORDS):
        return True
    if '%' in s and len(s) > 40:
        return True
    return False


def write_claims(claims, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(claims, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # demo: look for PDFs in demo/inputs and write demo/outputs/claims.json
    import os
    inp = os.path.join('demo', 'inputs')
    paths = []
    if os.path.isdir(inp):
        for f in os.listdir(inp):
            if f.lower().endswith('.pdf'):
                paths.append(os.path.join(inp, f))
    claims = extract(paths)
    out = os.path.join('demo', 'outputs', 'claims.json')
    write_claims(claims, out)
    print(f'Wrote {out} with {len(claims)} claims')