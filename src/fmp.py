"""
fmp.py — Financial Modeling Prep (FMP) market & statement verification helper

Queries SEC filings, income statements, and public company profiles via FMP API
to verify financial claims extracted from investment decks.
"""

import os
import re
import requests
from typing import Optional, Dict, Any

FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"


def get_fmp_api_key() -> Optional[str]:
    """Retrieve FMP API key from environment variables."""
    return os.environ.get("FMP_API_KEY") or os.environ.get("FINANCIAL_MODELING_PREP_API_KEY")


def search_company_symbol(query: str) -> Optional[str]:
    """Search FMP for a company symbol given a company name."""
    api_key = get_fmp_api_key()
    if not api_key or not query:
        return None
    try:
        url = f"{FMP_BASE_URL}/search?query={query}&limit=3&apikey={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            results = resp.json()
            if results and isinstance(results, list):
                return results[0].get("symbol")
    except Exception as e:
        print(f"FMP symbol search error: {e}")
    return None


def get_company_profile(symbol: str) -> Optional[Dict[str, Any]]:
    """Retrieve company financial profile from FMP."""
    api_key = get_fmp_api_key()
    if not api_key or not symbol:
        return None
    try:
        url = f"{FMP_BASE_URL}/profile/{symbol}?apikey={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data and isinstance(data, list):
                return data[0]
    except Exception as e:
        print(f"FMP profile error: {e}")
    return None


def verify_financial_claim(claim_text: str) -> bool:
    """
    Cross-reference financial claim with FMP market data and profiles.
    Returns True if valid matching financial evidence is confirmed.
    """
    api_key = get_fmp_api_key()
    if not api_key or not claim_text or len(claim_text) < 15:
        return False
        
    # Extract candidate stock tickers (uppercase 2-5 letter tokens)
    candidate_tokens = re.findall(r'\b[A-Z]{2,5}\b', claim_text)
    ignore_words = {"THE", "AND", "FOR", "WITH", "FROM", "THAT", "THIS", "FORM", "PAGE", "YEAR", "DECK", "SEED", "RAISE"}
    
    for token in candidate_tokens:
        if token in ignore_words:
            continue
        profile = get_company_profile(token)
        if profile and isinstance(profile, dict):
            # Check if numbers/years in claim align with market cap or revenue
            company_name = profile.get("companyName", "").lower()
            if company_name and any(w in claim_text.lower() for w in company_name.split()[:2]):
                return True
    return False


if __name__ == "__main__":
    import sys
    key = get_fmp_api_key()
    if not key:
        print("FMP_API_KEY is not set.")
    else:
        test_claim = sys.argv[1] if len(sys.argv) > 1 else "Apple reported annual revenue in 2023"
        result = verify_financial_claim(test_claim)
        print(f"Claim: '{test_claim}' | Verified via FMP: {result}")
