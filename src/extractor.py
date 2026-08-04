"""
extractor.py — stub for claim extraction

Functions to implement:
- extract(pdf_paths) -> list of claims (dicts with claim, source_file, page, type)
- write_claims(claims, out_path)
"""

import json


def extract(pdf_paths):
    """Placeholder extractor that returns an empty list.
    Replace with a model call that accepts multiple PDFs in one request.
    """
    return []


def write_claims(claims, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(claims, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # demo: write an empty claims.json
    write_claims([], 'claims.json')
    print('Wrote claims.json (stub)')