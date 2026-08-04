"""
memo.py — produce memo markdown from claims_checked.json
"""
import json
from datetime import datetime


def memo_from_checked(checked_path='claims_checked.json', out='memo.md'):
    with open(checked_path, 'r', encoding='utf-8') as f:
        checked = json.load(f)
    now = datetime.utcnow().isoformat() + 'Z'
    lines = [f"# Memo — generated {now}\n"]
    lines.append("## Key findings\n")
    verified = [c for c in checked if c.get('status') == 'verified']
    contradicted = [c for c in checked if c.get('status') == 'contradicted']
    unverifiable = [c for c in checked if c.get('status') == 'unverifiable']
    lines.append(f"- Verified claims: {len(verified)}")
    lines.append(f"- Contradicted claims: {len(contradicted)}")
    lines.append(f"- Unverifiable claims: {len(unverifiable)}\n")
    lines.append("---\n")
    lines.append("## Verified claims (sample)\n")
    for c in verified[:10]:
        lines.append(f"- {c.get('claim')} — {c.get('source_file')} p{c.get('page')}")
    lines.append('\n## Unverifiable / Questions\n')
    for c in unverifiable[:20]:
        lines.append(f"- {c.get('claim')} — ask: Is this accurate? Source: {c.get('source_file')} p{c.get('page')}")
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote memo to {out}')


if __name__ == '__main__':
    memo_from_checked()
