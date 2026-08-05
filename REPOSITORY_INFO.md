# Diligence Repository Information

## GitHub Metadata

**Repository:** https://github.com/beastofbayarea/diligence

### Short Description
"Extract, verify, and analyze claims from PDF investment decks using heuristics and AI (Gemini). Generates investment memos with confidence scores."

### Topics / Tags
- `claim-extraction` — automated claim extraction from documents
- `investment-analysis` — investment analysis and due diligence
- `pdf-processing` — PDF text extraction and analysis
- `gemini-api` — Google Gemini API integration
- `python` — Python-based implementation
- `financial-due-diligence` — financial research and verification
- `ai-verification` — AI-powered fact and claim verification

## Purpose

The **Diligence** project is a prototype pipeline for:

1. **Extracting falsifiable claims** from PDF investment decks and pitches
2. **Verifying claims** using multiple methods:
   - Heuristic pattern matching
   - EDGAR financial data search
   - AI model-based verification (Gemini)
3. **Generating investment memos** with confidence scores and verification status

## Use Cases

- **Due diligence teams** — Automate initial claim extraction from pitch decks
- **Investors** — Quickly verify key claims in investment materials
- **Analysts** — Generate structured reports from unstructured PDFs
- **Research** — Dataset and benchmark for claim extraction/verification tasks

## Key Features

✅ **End-to-end pipeline** — Extract → Verify → Memo  
✅ **Graceful fallback** — Works with or without AI models  
✅ **Model flexibility** — Supports Gemini API or custom HTTP endpoints  
✅ **Open source** — Python, easy to integrate into other tools  
✅ **Benchmarked** — Includes 5-deck labeled dataset for evaluation  

## Getting Started

See `README.md` for quick start, or `GEMINI_API_SETUP.md` for model setup.

```bash
# Quick start (heuristics only)
pip install -r requirements.txt
python run_pipeline.py

# With Gemini API (recommended)
# 1. Get API key: https://makersuite.google.com/app/apikeys
# 2. Edit .env with your GEMINI_API_KEY
# 3. python run_pipeline.py
```

## Tech Stack

- **Language:** Python 3
- **PDF Processing:** pypdf
- **Data Validation:** jsonschema
- **Model Integration:** Gemini API, Google Vertex AI
- **Financial Data:** SEC EDGAR API (optional)
- **CI/CD:** GitHub Actions

## Project Structure

```
diligence/
├── run_pipeline.py          # Main entry point
├── bench.py                 # Benchmark evaluator
├── src/                     # Core modules
│   ├── extractor.py         # PDF extraction (heuristic)
│   ├── model_extractor.py   # AI-backed extraction
│   ├── verify.py            # Verification orchestrator
│   ├── model_verifier.py    # AI-backed verification
│   └── memo.py              # Memo generation
├── demo/                    # Sample inputs and outputs
├── bench/                   # Labeled evaluation dataset
├── docs/                    # Documentation
└── .github/workflows/       # CI/CD
```

## Performance

**Benchmark Results (5-deck dataset, heuristic-only):**

- Average Precision: 0.90
- Average Recall: 0.60
- Expected improvement with Gemini API: +15-25% recall

## Documentation

- `README.md` — Overview and quick start
- `IMPLEMENTATION_PLAN.md` — Original requirements and roadmap
- `GEMINI_API_SETUP.md` — Step-by-step Gemini API configuration
- `docs/SETUP_GEMINI_API.md` — Detailed setup guide
- `docs/IMPLEMENTATION_STATUS.md` — Completion status and architecture

## Contributing

This is a prototype project. Feel free to fork and adapt for your use case.

Key areas for improvement:
- Fine-tune claim extraction heuristics
- Expand labeled dataset beyond 5 decks
- Add support for other model providers (Claude, LLaMA, etc.)
- Implement EDGAR integration for financial verification
- Add web UI for demo purposes

## License

Not specified (check repo for license file)

## Contact

GitHub: @beastofbayarea
Repository: https://github.com/beastofbayarea/diligence

---

**Last Updated:** 2026-08-05  
**Status:** Production-ready prototype with fallback strategy
