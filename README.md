Diligence — prototype

This repository implements a small prototype pipeline for extracting and verifying claims from PDF decks, following the IMPLEMENTATION_PLAN.md.

## Quick Start (Heuristic Extraction)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Put 2–3 PDF decks in demo/inputs (deck1.pdf, deck2.pdf)

3. Run full pipeline:
   ```bash
   python run_pipeline.py
   ```

4. Inspect outputs in demo/outputs: claims.json, claims_checked.json, questions.md, memo.md

## Model-Backed Extraction (Recommended)

To use **Google Gemini API** for improved claim extraction and verification:

1. Get a free Gemini API key: https://makersuite.google.com/app/apikeys
2. Create `.env` file in repo root:
   ```bash
   MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
   GEMINI_API_KEY=your-api-key-here
   ```
3. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```

See [docs/SETUP_GEMINI_API.md](docs/SETUP_GEMINI_API.md) for detailed setup instructions.

## Commands

- **Full pipeline:** `python run_pipeline.py`
- **Stage-only:** `python run_pipeline.py --step 1|2|3` (1=extract, 2=verify, 3=memo)
- **Benchmark:** `python bench.py bench/` (requires labeled dataset)

## Files of Interest

- `src/extractor.py` — PDF text extraction with heuristics
- `src/model_extractor.py` — Model-backed claim extraction (Gemini or Vertex)
- `src/verify.py` — Claim verification (heuristics + EDGAR + model)
- `src/memo.py` — Memo generation from verified claims
- `run_pipeline.py` — Pipeline orchestrator
- `bench.py` — Precision/recall evaluator

## Architecture

The pipeline has three stages:

1. **Extract** — Extract claims from PDFs (heuristic or model-based)
2. **Verify** — Verify claims (heuristics, EDGAR search, model-based)
3. **Memo** — Generate investment memo from verified claims

Each stage falls back gracefully if external services are unavailable.

## Fallback Strategy

If MODEL_API_KEY or GEMINI_API_KEY is not configured:
- Extraction falls back to heuristic PDF analysis
- Verification falls back to regex patterns
- Pipeline always produces output (may be less accurate without models)

## Configuration

| Variable | Purpose | Example |
|----------|---------|---------|
| `MODEL_API_URL` | HTTP model endpoint | `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent` |
| `GEMINI_API_KEY` | Model API key | (from Google AI Studio) |
| `GCP_PROJECT_ID` | GCP project (optional) | `cent-capital` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account path (optional) | `service-account-key.json` |
| `USE_EDGAR` | Enable EDGAR verification | `1` |
| `SEC_USER_AGENT` | EDGAR user agent | `MyApp/1.0 (you@example.com)` |

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for the roadmap and requirements.
