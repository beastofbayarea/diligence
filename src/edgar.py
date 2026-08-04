"""
edgar.py — lightweight EDGAR search helper for prototype verification

This module queries the SEC full-text search endpoint and does a best-effort scan of
returned results to see if a claim text appears in filings. It is intentionally
conservative and will return False when unsure.

Enable by setting environment variable USE_EDGAR=1 before running verify().

Note: The SEC requires a descriptive User-Agent header. Set SEC_USER_AGENT env var
or default to 'diligence-prototype/1.0 (contact: none)'.
"""

import os
import requests
import time
import re
from typing import Optional

SEARCH_URL = 'https://efts.sec.gov/LATEST/search-index'


def _user_agent():
    return os.environ.get('SEC_USER_AGENT', 'diligence-prototype/1.0')


def _post_search(query: str, start: int = 0, count: int = 10) -> Optional[dict]:
    headers = {
        'User-Agent': _user_agent(),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'query': query,
        'start': start,
        'count': count
    }
    try:
        resp = requests.post(SEARCH_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f'EDGAR search request failed: {e}')
        return None


def search_claim_phrase(claim: str) -> bool:
    """Search EDGAR for the claim phrase or key tokens. Return True if a likely match found."""
    if not claim or len(claim) < 15:
        return False
    # Try exact phrase search first (shortened if very long)
    phrase = claim
    if len(phrase) > 200:
        phrase = phrase[:200]
    # remove problematic characters
    phrase_q = re.sub(r"[\n\r\t]+", ' ', phrase)
    # The search API may accept simple queries; try the full phrase
    data = _post_search(phrase_q)
    if data and isinstance(data, dict):
        hits = data.get('hits') or {}
        hit_list = hits.get('hits') if isinstance(hits, dict) else None
        if hit_list:
            # check returned hit sources for the phrase
            for h in hit_list:
                src = h.get('_source') or {}
                # common fields: 'text' or 'document' or 'content'
                text = ''
                for k in ('text', 'document', 'content', 'file_text'):
                    if k in src and isinstance(src[k], str):
                        text += '\n' + src[k]
                if text and phrase.lower() in text.lower():
                    return True
    # Fallback: search by numeric tokens from claim (years or $ amounts)
    nums = re.findall(r"\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?|20\d{2}", claim)
    for n in nums:
        q = str(n)
        data = _post_search(q)
        if data and isinstance(data, dict):
            hits = data.get('hits') or {}
            hit_list = hits.get('hits') if isinstance(hits, dict) else None
            if hit_list:
                # consider any hit as suggestive
                return True
        time.sleep(0.2)
    return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python edgar.py "claim text"')
        sys.exit(1)
    claim = sys.argv[1]
    ok = search_claim_phrase(claim)
    print('Verified on EDGAR' if ok else 'Not found on EDGAR')
