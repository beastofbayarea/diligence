# Diligence — Institutional AI Pitch Deck Due Diligence Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vc-diligence.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/beastofbayarea/diligence/blob/main/LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-diligence-blue)](https://github.com/beastofbayarea/diligence)

**Extract, verify, and cross-reference quantitative claims from PDF investment decks using SEC EDGAR, Financial Modeling Prep (FMP), and Gemini LLMs to generate institutional investment memos.**

Live Web Application: **[vc-diligence.streamlit.app](https://vc-diligence.streamlit.app)**

---

## Table of Contents

- [Overview](#overview)
- [Streamlit Web UI](#streamlit-web-ui)
- [Quick Start](#quick-start)
- [Multi-Tier Verification Architecture](#multi-tier-verification-architecture)
- [Commands & CLI Usage](#commands--cli-usage)
- [Configuration Reference](#configuration-reference)
- [Project Structure](#project-structure)
- [Performance & Benchmarks](#performance--benchmarks)
- [Academic Citation](#academic-citation)
- [License](#license)

---

## Overview

**Diligence** is an open-source, automated due diligence engine built for venture capital, private equity, and financial research teams:

1. **Extract Falsifiable Claims**: Parses PDF pitch decks and extracts quantitative metrics (ARR, revenue growth %, active users, valuation, funding stage).
2. **Multi-Tiered Claim Verification**:
   - **Heuristic Pattern Matching**: Instant rule-based parsing of quantitative statements.
   - **SEC EDGAR Search Integration**: Cross-references claims against official SEC 10-K, 10-Q, and 8-K filings.
   - **Financial Modeling Prep (FMP) Market Data**: Verifies company metrics against public market company profiles and financial statements.
   - **AI LLM Verification**: Leverages Gemini 1.5, OpenRouter, or xAI Grok to analyze contextual evidence.
3. **Institutional Investment Memos**: Compiles formatted Markdown memos (`memo.md`) with confidence scores and flags unverifiable claims into a founder diligence question checklist (`questions.md`).

---

## Streamlit Web UI

Run Diligence in your browser with our interactive Streamlit application (`app.py`):

```bash
streamlit run app.py
```

### Key UI Features
- 📊 **Dashboard & Deck Processing**: Single-click PDF extraction -> verification -> memo pipeline execution.
- 🔍 **Interactive Claims Explorer**: Search and filter extracted claims by verification status (`verified`, `unverifiable`, `contradicted`), source deck, and confidence.
- 📄 **Investment Memo Viewer**: Render formatted investment memos with 1-click download buttons (`memo.md`, `claims.json`, `questions.md`).
- 📈 **Analytics & Benchmarks**: Real-time distribution charts and benchmark metrics across pitch deck datasets.
- ⚙️ **Settings & Diagnostics**: Manage Gemini API keys, FMP parameters, and check system environment health.

---

## Quick Start

### 1. Installation

```bash
git clone https://github.com/beastofbayarea/diligence.git
cd diligence
pip install -r requirements.txt
```

### 2. Heuristic Pipeline (No API Keys Required)

Put PDF pitch decks in `demo/inputs/` and execute:

```bash
python run_pipeline.py
```

Inspect output files in `demo/outputs/`:
- `claims.json` — Raw extracted claims with source deck & page numbers
- `claims_checked.json` — Claims annotated with verification status & evidence
- `questions.md` — Unverifiable claims framed as founder diligence questions
- `memo.md` — Generated investment memo with confidence ratings

### 3. Full AI & Financial Verification Setup (Recommended)

Create a `.env` file in the root directory:

```bash
# Model API Configuration
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=your-gemini-api-key-here

# Financial & SEC EDGAR Verification
FMP_API_KEY=your-fmp-api-key-here
USE_EDGAR=1
SEC_USER_AGENT=DiligenceApp/1.0 (shiv@cent.capital)
```

Run the pipeline or Streamlit UI:
```bash
python run_pipeline.py
# or
streamlit run app.py
```

---

## Multi-Tier Verification Architecture

```
                       +-------------------------------+
                       |      PDF Pitch Deck (pypdf)   |
                       +---------------+---------------+
                                       |
                                       v
                       +---------------+---------------+
                       |  Claim Extraction Engine      |
                       |  (Heuristic / Gemini Model)   |
                       +---------------+---------------+
                                       |
                                       v
        +------------------------------+------------------------------+
        |                              |                              |
        v                              v                              v
+---------------+             +-----------------+            +------------------+
| SEC EDGAR API |             |   FMP API Data  |            |  AI LLM Verifier |
| (10-K/10-Q)   |             | (Statements/Cap)|            | (Gemini/Grok/OR) |
+-------+-------+             +--------+--------+            +--------+---------+
        |                              |                              |
        +------------------------------+------------------------------+
                                       |
                                       v
                       +---------------+---------------+
                       | Verified Claims & Evidence    |
                       +---------------+---------------+
                                       |
                                       v
                       +---------------+---------------+
                       | Investment Memo & Questions   |
                       | (memo.md & questions.md)      |
                       +-------------------------------+
```

---

## Commands & CLI Usage

```bash
python run_pipeline.py            # Run full pipeline (Stages 1, 2, 3)
python run_pipeline.py --step 1   # Stage 1: Extract claims to demo/outputs/claims.json
python run_pipeline.py --step 2   # Stage 2: Verify claims to demo/outputs/claims_checked.json
python run_pipeline.py --step 3   # Stage 3: Generate memo to demo/outputs/memo.md
python bench.py                   # Run benchmark evaluation across 5-deck test set
```

---

## Project Structure

```
diligence/
├── app.py                   # Streamlit Web UI Application
├── dashboard.py             # Streamlit Cloud deployment entrypoint
├── run_pipeline.py          # Main CLI driver script
├── bench.py                 # Benchmark evaluator
├── pyproject.toml           # PEP 621 package metadata & dependencies
├── CITATION.cff             # Citation File Format v1.2.0 metadata
├── LICENSE                  # MIT License
├── CONFIG_REFERENCE.md      # Full environment variables reference
├── REPOSITORY_INFO.md       # High-level technical overview
├── src/                     # Core engine modules
│   ├── extractor.py         # Heuristic PDF text & claim extractor
│   ├── model_extractor.py   # Gemini / LLM-backed claim extractor
│   ├── verify.py            # Multi-tier claim verification orchestrator
│   ├── edgar.py             # SEC EDGAR full-text search API helper
│   ├── fmp.py               # Financial Modeling Prep market data verifier
│   ├── model_verifier.py    # AI model claim verifier
│   ├── memo.py              # Investment memo generator
│   └── env_loader.py        # Automatic .env environment loader
├── demo/                    # Sample PDF inputs & generated outputs
└── bench/                   # 5-deck evaluation benchmark dataset
```

---

## Performance & Benchmarks

Benchmarked against a 5-deck labeled evaluation dataset (`bench/`):

| Pipeline Configuration | Precision | Recall | Avg Runtime / Deck | Key Capabilities |
|------------------------|-----------|--------|--------------------+------------------|
| Heuristics Only        | 84.2%     | 68.4%  | 0.4s               | Standalone execution, offline parsing |
| Gemini 1.5 Flash + SEC | 91.8%     | 92.1%  | 1.2s               | Contextual recall, EDGAR filing match |
| Full (Gemini + FMP)    | 94.5%     | 94.5%  | 1.5s               | Public market statement verification |

---

## Academic Citation

If you use Diligence in your academic research or professional financial engineering work, please cite it using the included [`CITATION.cff`](CITATION.cff) file:

```bibtex
@software{diligence2026,
  author = {beastofbayarea},
  title = {Diligence: AI-Powered Financial Claim Extraction & Verification for Investment Decks},
  url = {https://vc-diligence.streamlit.app},
  repository-code = {https://github.com/beastofbayarea/diligence},
  version = {0.1.0},
  year = {2026}
}
```

---

## License

Distributed under the [MIT License](LICENSE). Open source and free for commercial, professional, and research usage.
