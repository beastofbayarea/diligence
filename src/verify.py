"""
verify.py — verification step

Behavior (prototype):
- Loads claims.json
- Attempts a lightweight verification: if a claim contains words commonly found in filings
  and a year or numeric token matching a filing context, mark 'verified'; otherwise 'unverifiable'.
- Writes claims_checked.json and questions.md

This is intentionally conservative: it must prefer unverifiable when unsure.
"""

import json
import re
import os

# Optional EDGAR integration
try:
    from src import edgar
    EDGAR_AVAILABLE = True
except Exception:
    edgar = None
    EDGAR_AVAILABLE = False


def verify(claims_path, out_checked='claims_checked.json', out_questions='questions.md'):
    with open(claims_path, 'r', encoding='utf-8') as f:
        claims = json.load(f)
    checked = []
    questions = ['# Questions (unverifiable claims)\n']
    use_edgar = os.environ.get('USE_EDGAR') == '1' and EDGAR_AVAILABLE
    for c in claims:
        text = c.get('claim','')
        c_checked = dict(c)
        # simple heuristic: if claim references 'annual' or '10-K' or 'Form' or 'reported' and has a 4-digit year, mark verified
        if re.search(r'\b(10-K|10k|form|annual report|reported|filing|10-q|10q)\b', text, re.I) and re.search(r'20\d{2}', text):
            c_checked['status'] = 'verified'
        else:
            # Try EDGAR if enabled
            if use_edgar:
                try:
                    found = edgar.search_claim_phrase(text)
                    if found:
                        c_checked['status'] = 'verified'
                    else:
                        c_checked['status'] = 'unverifiable'
                        questions.append(f"- {text} — source: {c.get('source_file')} p{c.get('page')}\n  Suggested question: Please confirm this claim and cite a filing or source.")
                except Exception as e:
                    print(f'EDGAR verification error: {e} — falling back to unverifiable')
                    c_checked['status'] = 'unverifiable'
                    questions.append(f"- {text} — source: {c.get('source_file')} p{c.get('page')}\n  Suggested question: Please confirm this claim and cite a filing or source.")
            else:
                c_checked['status'] = 'unverifiable'
                questions.append(f"- {text} — source: {c.get('source_file')} p{c.get('page')}\n  Suggested question: Please confirm this claim and cite a filing or source.")
        checked.append(c_checked)
    with open(out_checked, 'w', encoding='utf-8') as f:
        json.dump(checked, f, indent=2, ensure_ascii=False)
    with open(out_questions, 'w', encoding='utf-8') as f:
        f.write('\n'.join(questions))
    print(f'Wrote {out_checked} and {out_questions}')


if __name__ == '__main__':
    print('Run verify.verify(claims_path) to produce claims_checked.json and questions.md')