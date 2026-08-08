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

# Optional EDGAR & FMP integrations
try:
    from src import edgar
    EDGAR_AVAILABLE = True
except Exception:
    edgar = None
    EDGAR_AVAILABLE = False

try:
    from src import fmp
    FMP_AVAILABLE = True
except Exception:
    fmp = None
    FMP_AVAILABLE = False


def verify(claims_path, out_checked='claims_checked.json', out_questions='questions.md'):
    with open(claims_path, 'r', encoding='utf-8') as f:
        claims = json.load(f)
    checked = []
    questions = ['# Questions (unverifiable claims)\n']
    use_edgar = os.environ.get('USE_EDGAR') == '1' and EDGAR_AVAILABLE
    use_fmp = FMP_AVAILABLE and bool(os.environ.get('FMP_API_KEY') or os.environ.get('FINANCIAL_MODELING_PREP_API_KEY'))
    
    # Prepare for optional model-based verification
    try:
        from src import model_verifier
    except Exception:
        model_verifier = None
    # If model verifier available and EDGAR not used, we can send batch verification
    model_checks = None
    if use_edgar is False and model_verifier is not None:
        try:
            model_checks = model_verifier.verify_with_model(claims)
        except Exception:
            model_checks = None
    for c in claims:
        text = c.get('claim','')
        c_checked = dict(c)
        # simple heuristic: if claim references 'annual' or '10-K' or 'Form' or 'reported' and has a 4-digit year, mark verified
        if re.search(r'\b(10-K|10k|form|annual report|reported|filing|10-q|10q)\b', text, re.I) and re.search(r'20\d{2}', text):
            c_checked['status'] = 'verified'
        else:
            found = False
            if use_fmp:
                try:
                    found = fmp.verify_financial_claim(text)
                    if found:
                        c_checked['status'] = 'verified'
                        c_checked['evidence'] = 'Verified via Financial Modeling Prep (FMP) market data'
                except Exception as e:
                    print(f'FMP verification error: {e} — continuing')
            if not found and use_edgar:
                try:
                    found = edgar.search_claim_phrase(text)
                    if found:
                        c_checked['status'] = 'verified'
                except Exception as e:
                    print(f'EDGAR verification error: {e} — continuing')
            if not found and model_checks is not None:
                # model_checks maps claim text -> {status, evidence}
                m = model_checks.get(text)
                if m:
                    stat = m.get('status')
                    if stat in ('verified','contradicted','unverifiable'):
                        c_checked['status'] = stat
                        if m.get('evidence'):
                            c_checked['evidence'] = m.get('evidence')
                        found = True
            if not found:
                c_checked['status'] = 'unverifiable'
                # only add question for unverifiable
                questions.append(f"- {text} — source: {c.get('source_file')} p{c.get('page')}\n  Suggested question: Please confirm this claim and cite a filing or source.")
        checked.append(c_checked)
    with open(out_checked, 'w', encoding='utf-8') as f:
        json.dump(checked, f, indent=2, ensure_ascii=False)
    with open(out_questions, 'w', encoding='utf-8') as f:
        f.write('\n'.join(questions))
    print(f'Wrote {out_checked} and {out_questions}')


if __name__ == '__main__':
    print('Run verify.verify(claims_path) to produce claims_checked.json and questions.md')