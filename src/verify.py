"""
verify.py — stub for verification step

Functions to implement:
- verify(claims_path) -> writes claims_checked.json and questions.md
"""

import json


def verify(claims_path, out_checked='claims_checked.json', out_questions='questions.md'):
    # Minimal placeholder: copy claims to checked with status 'unverifiable'
    with open(claims_path, 'r', encoding='utf-8') as f:
        claims = json.load(f)
    checked = []
    questions = ['# Questions (auto-generated)\n']
    for c in claims:
        c_checked = dict(c)
        c_checked['status'] = 'unverifiable'
        checked.append(c_checked)
        questions.append(f"- {c.get('claim','(no claim)')} — question: Verify this claim\n")
    with open(out_checked, 'w', encoding='utf-8') as f:
        json.dump(checked, f, indent=2, ensure_ascii=False)
    with open(out_questions, 'w', encoding='utf-8') as f:
        f.write('\n'.join(questions))


if __name__ == '__main__':
    print('verify.py stub — implement EDGAR search and second model pass.')