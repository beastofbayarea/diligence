# Diligence Repository Information

## GitHub Metadata

**Repository:** https://github.com/beastofbayarea/diligence  
**Live Streamlit App:** https://vc-diligence.streamlit.app  

### Short Description
"⚡ Institutional AI due diligence engine. Extract, verify, & cross-reference falsifiable claims from PDF investment decks using SEC EDGAR, FMP, & Gemini LLMs to generate investment memos."

### Topics / Tags
- `ai-due-diligence` — AI-powered investment due diligence automation
- `investment-analysis` — financial due diligence and pitch deck evaluation
- `claim-extraction` — automated quantitative claim extraction from PDF decks
- `sec-edgar` — SEC EDGAR financial filing search integration
- `financial-modeling-prep` — FMP public company financial data verification
- `gemini-api` — Google Gemini 1.5 LLM integration for model-backed extraction
- `streamlit` — interactive Streamlit web dashboard UI (`app.py`)
- `pdf-parsing` — PDF text extraction with pypdf
- `financial-technology` — FinTech & venture capital automation tools
- `venture-capital` — institutional VC pitch deck diligence
- `investment-memos` — automated markdown memo generation
- `llm-verification` — AI-powered claim cross-examination
- `python` — Python 3.10+ open-source codebase
- `open-source` — MIT licensed financial engineering software

---

## Purpose

The **Diligence** project is an institutional-grade pipeline for:

1. **Extracting falsifiable claims** from PDF investment decks and pitch materials.
2. **Verifying claims** using multi-tiered verification methods:
   - Heuristic pattern matching & quantitative validation
   - SEC EDGAR full-text search integration (`src/edgar.py`)
   - Financial Modeling Prep (FMP) market & statement cross-referencing (`src/fmp.py`)
   - AI model-backed claim verification (Gemini 1.5, OpenRouter, Grok / xAI)
3. **Generating institutional investment memos** with confidence scores, risk flags, and founder diligence question lists.
4. **Interactive Web UI**: Streamlit web application (`app.py` / `dashboard.py`) deployed live.

---

## Use Cases

- **Venture Capital & Private Equity** — Automate initial pitch deck screening and quantitative claim verification.
- **Angel Investors** — Instantly verify traction metrics (ARR, MRR, growth %) against public records.
- **Financial Engineers & Analysts** — Generate structured due diligence markdown reports from unstructured PDFs.
- **Academic & Industry Research** — Citeable reference framework (`CITATION.cff`) for claim verification bench testing.

---

## Key Features

✅ **End-to-end Automated Pipeline** — Extract → Verify → Memo  
✅ **Multi-Tiered Verification Engine** — Heuristics + SEC EDGAR + FMP Market Data + Gemini / LLMs  
✅ **Interactive Streamlit Web UI** — Single-click pipeline runner, filterable claims table, and memo downloader  
✅ **Graceful Fallback & Multi-Model Support** — Operates seamlessly with or without API keys  
✅ **Standard Metadata & Open Source** — MIT Licensed, PEP 621 `pyproject.toml`, CFF Citation v1.2.0  

---

## Getting Started

```bash
# 1. Clone repository & install dependencies
git clone https://github.com/beastofbayarea/diligence.git
cd diligence
pip install -r requirements.txt

# 2. Run CLI Pipeline
python run_pipeline.py

# 3. Launch Local Streamlit Dashboard
streamlit run app.py
```

---

## Tech Stack

- **Language:** Python 3.10+
- **Web UI:** Streamlit (`app.py` & `dashboard.py`)
- **PDF Processing:** pypdf
- **Data Validation:** jsonschema, pandas
- **Model Integration:** Gemini API, Google Vertex AI, OpenRouter, Grok / xAI
- **Financial Data APIs:** SEC EDGAR API, Financial Modeling Prep (FMP) API, FRED API
- **Package Spec:** PEP 621 `pyproject.toml`
- **CI/CD & Deployment:** GitHub Actions, Streamlit Cloud

---

## Project Structure

```
diligence/
├── app.py                   # Streamlit Web Application
├── dashboard.py             # Streamlit Cloud deployment entrypoint
├── run_pipeline.py          # Main CLI driver script
├── bench.py                 # Benchmark evaluator
├── pyproject.toml           # PEP 621 package metadata
├── CITATION.cff             # Citation File Format v1.2.0
├── LICENSE                  # MIT License
├── src/                     # Core pipeline modules
│   ├── extractor.py         # Heuristic PDF claim extractor
│   ├── model_extractor.py   # AI-backed claim extractor
│   ├── verify.py            # Multi-tiered verification orchestrator
│   ├── edgar.py             # SEC EDGAR full-text search integration
│   ├── fmp.py               # Financial Modeling Prep market data verifier
│   ├── model_verifier.py    # AI model claim verifier
│   ├── memo.py              # Investment memo generator
│   └── env_loader.py        # Environment variables auto-loader
├── demo/                    # Sample PDF inputs & demo outputs
└── bench/                   # 5-deck evaluation benchmark dataset
```

---

## Documentation Links

- `README.md` — Complete documentation, quick start, architecture, & badges
- `CONFIG_REFERENCE.md` — Environment variables & setup reference
- `FEATURE_ROADMAP_RICE.md` — RICE framework feature roadmap
- `CITATION.cff` — Academic / professional citation metadata

---

## License

[MIT License](LICENSE) — Open source, free for academic and commercial usage.

## Contact & Repository

- **Author / Maintainer:** @beastofbayarea
- **Repository:** https://github.com/beastofbayarea/diligence
- **Live App:** https://vc-diligence.streamlit.app
