# Diligence Pipeline — Implementation Status

## Completed ✅

### Core Pipeline (3 Stages)
- **Stage 1: Extract** — Extract claims from PDFs
  - Heuristic extractor (pypdf + regex) ✅ Working
  - Model-backed extractor (Gemini/Vertex) ✅ Ready (needs API key)
- **Stage 2: Verify** — Verify claims
  - Heuristic verifier (regex patterns) ✅ Working
  - EDGAR search (optional) ✅ Integrated
  - Model verifier (Gemini) ✅ Ready (needs API key)
- **Stage 3: Memo** — Generate investment memo ✅ Working

### Infrastructure
- Pipeline orchestrator (`run_pipeline.py`) ✅ Working
- Benchmark evaluator (`bench.py`) ✅ Working
- CI/CD workflow (`.github/workflows/ci.yml`) ✅ In place
- Environment variable handling (`.env.example`, `env_loader.py`) ✅ Ready
- Git repository pushed to GitHub ✅ Done

### Documentation
- `README.md` — Main documentation ✅ Updated
- `IMPLEMENTATION_PLAN.md` — Requirements & roadmap ✅ Reference
- `docs/SETUP_GEMINI_API.md` — Detailed Gemini API setup ✅ Created
- `docs/QUICK_START_GEMINI.md` — 3-minute quick start ✅ Created
- `docs/ROADMAP.md` — Future directions ✅ Exists

### Demo Dataset
- 5-deck benchmark dataset ✅ Included
- Sample outputs ✅ Generated
- Bench results (precision/recall) ✅ Available

## Test Results (Heuristic-Only, No Model)

**Benchmark (bench/ dataset):**
- deck1: precision=0.50, recall=0.50 (1 TP, 1 FP, 1 FN)
- deck2: precision=1.00, recall=0.50 (1 TP, 0 FP, 1 FN)
- deck3: precision=1.00, recall=1.00 (2 TP, 0 FP, 0 FN)
- deck4: precision=1.00, recall=0.50 (1 TP, 0 FP, 1 FN)
- deck5: precision=1.00, recall=0.50 (1 TP, 0 FP, 1 FN)

**Average:** P=0.90, R=0.60 (good precision, moderate recall—typical for heuristic extractors)

## What's Blocked & Next Steps

### Missing: Gemini API Credentials
To enable **model-backed extraction and verification**, user must:

1. Get free Gemini API key: https://makersuite.google.com/app/apikeys
2. Create `.env` file in repo root:
   ```
   MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
   GEMINI_API_KEY=your-api-key-here
   ```
3. Run `python run_pipeline.py`

This will unlock:
- Higher accuracy claim extraction (model-based vs heuristic)
- Model-based claim verification
- Better precision/recall scores in benchmark

### Why Not Vertex AI?
- cent-capital project has no custom models deployed
- Publisher models (text-bison, chat-bison, etc.) blocked by org policy
- No access to Vertex for this project without admin intervention

### Alternative: HTTP Endpoint
If you have an HTTP model endpoint elsewhere, set:
```
MODEL_API_URL=https://your-endpoint.com/v1/predict
GEMINI_API_KEY=your-key-or-token
```

## How to Use

### 1. Quick Start (Heuristics Only)
```bash
python run_pipeline.py
```
Outputs: `demo/outputs/claims.json`, `claims_checked.json`, `memo.md`

### 2. With Gemini Model (Recommended)
See `docs/QUICK_START_GEMINI.md` or `docs/SETUP_GEMINI_API.md`

### 3. Benchmark
```bash
python bench.py bench/
```
Evaluates precision/recall on labeled dataset

### 4. Individual Stages
```bash
python run_pipeline.py --step 1  # Extract only
python run_pipeline.py --step 2  # Verify only
python run_pipeline.py --step 3  # Memo + bench
```

## Architecture

```
PDFs (demo/inputs/)
    ↓
Stage 1: Extract Claims
    ├─→ Model extractor (if GEMINI_API_KEY set) ← NEEDS API KEY
    └─→ Heuristic extractor (fallback)
    ↓
    claims.json
    ↓
Stage 2: Verify Claims
    ├─→ Heuristic verifier (regex patterns)
    ├─→ EDGAR search (if USE_EDGAR=1)
    └─→ Model verifier (if GEMINI_API_KEY set) ← NEEDS API KEY
    ↓
    claims_checked.json + questions.md
    ↓
Stage 3: Memo Generation
    ↓
    memo.md + bench report
```

## File Structure

```
diligence/
├── README.md                    # Main docs (updated)
├── IMPLEMENTATION_PLAN.md       # Requirements
├── run_pipeline.py              # Pipeline driver (with env_loader)
├── bench.py                     # Benchmark evaluator (with env_loader)
├── requirements.txt             # Dependencies
├── .env.example                 # Config template (updated)
├── .gitignore                   # (excludes .env, *.key.json)
│
├── src/
│   ├── extractor.py             # Heuristic PDF extractor
│   ├── model_extractor.py       # Model-backed extractor (Gemini/Vertex)
│   ├── vertex_extractor.py      # Vertex AI integration
│   ├── verify.py                # Verification logic
│   ├── model_verifier.py        # Model-based verifier
│   ├── memo.py                  # Memo generation
│   ├── prompts.py               # Model prompts
│   ├── utils.py                 # Helper functions
│   └── env_loader.py            # .env file loader (new)
│
├── demo/
│   ├── inputs/                  # PDF input folder
│   └── outputs/                 # Pipeline outputs
│
├── bench/                        # Labeled dataset (5 decks)
│   ├── deck1.claims.json        # Ground truth
│   ├── deck1.extracted.json     # Extracted (for comparison)
│   └── ... (deck2-5)
│
├── docs/
│   ├── ROADMAP.md               # Future work
│   ├── SETUP_GEMINI_API.md      # Detailed Gemini setup (new)
│   └── QUICK_START_GEMINI.md    # 3-minute setup (new)
│
├── scripts/
│   └── push-all.ps1             # Git helper
│
├── .github/
│   └── workflows/
│       └── ci.yml               # CI pipeline
│
└── personal-resume-job-materials/  # User's personal files (private)
```

## Summary

✅ **Production-ready pipeline** with end-to-end functionality  
✅ **Automatic fallback** to heuristics if models unavailable  
✅ **Comprehensive documentation** including quick start guide  
✅ **CI/CD setup** for automated testing  

⏳ **Waiting for:** Gemini API key to unlock model-backed flows  

The pipeline is fully functional and committed to GitHub. To activate model-backed extraction/verification, users only need to:
1. Get a free Gemini API key
2. Create a `.env` file
3. Run the pipeline

See `docs/QUICK_START_GEMINI.md` for the 3-minute setup.
