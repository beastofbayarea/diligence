Diligence — prototype

This repository implements a small prototype pipeline for extracting and verifying claims from PDF decks, following the IMPLEMENTATION_PLAN.md.

Quick start:

1. Install dependencies:
   pip install -r requirements.txt

2. Put 2–3 PDF decks in demo/inputs (deck1.pdf, deck2.pdf)

3. Run full pipeline:
   python run_pipeline.py

4. Inspect outputs in demo/outputs: claims.json, claims_checked.json, questions.md, memo.md

Commands:
- Stage-only: python run_pipeline.py --step 1|2|3
- Benchmark: python bench.py labeled_dir

Files of interest:
- src/extractor.py — PDF extractor (heuristic)
- src/verify.py — verification heuristics
- src/memo.py — memo generation
- run_pipeline.py — pipeline driver
- scripts/push-all.ps1 — helper to commit & push

See IMPLEMENTATION_PLAN.md for the roadmap and demo script.
## Vertex AI (Gemini) — model extraction

Configure environment (example .env or exported variables):

GCP_PROJECT_ID=cent-capital
GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
GCP_REGION=global
GEMINI_MODEL=gemini-flash-latest

Install the Vertex AI client:

pip install google-cloud-aiplatform

Run the model-backed extraction (pipeline prefers Vertex when configured):

python run_pipeline.py --step 1

Run the full pipeline:

python run_pipeline.py

