"""
utils.py — small utility helpers for console output and validation
"""
import json


def print_claims_table(claims):
    if not claims:
        print('No claims to show')
        return
    # determine column widths
    headers = ['#', 'claim', 'source_file', 'page', 'type']
    rows = []
    for i, c in enumerate(claims, start=1):
        rows.append([str(i), c.get('claim','')[:80].replace('\n',' '), c.get('source_file',''), str(c.get('page','')), c.get('type','')])
    col_widths = [max(len(r[i]) for r in ([headers] + rows)) for i in range(len(headers))]
    # print header
    hdr = ' | '.join(h.ljust(col_widths[i]) for i,h in enumerate(headers))
    print(hdr)
    print('-' * len(hdr))
    for r in rows:
        print(' | '.join(r[i].ljust(col_widths[i]) for i in range(len(r))))


def validate_schema(instance, schema):
    try:
        import jsonschema
    except Exception:
        print('jsonschema not installed; skipping schema validation')
        return True
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True
    except Exception as e:
        print(f'Schema validation failed: {e}')
        return False
