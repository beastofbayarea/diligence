# Diligence — Prototype

[![GitHub Repository](https://img.shields.io/badge/GitHub-diligence-blue)](https://github.com/beastofbayarea/diligence)
[![Python](https://img.shields.io/badge/Python-3-blue)](https://python.org)

**Extract, verify, and analyze claims from PDF investment decks using heuristics and AI (Gemini). Generates investment memos with confidence scores.**

A working prototype demoable in ten minutes that survives follow-up questions. Built backwards from the demo, not forwards from the architecture.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Model-Backed Extraction](#model-backed-extraction-recommended)
- [Architecture](#architecture)
- [Commands](#commands)
- [Configuration Reference](#configuration-reference)
- [Project Structure](#project-structure)
- [Performance](#performance--benchmarking)
- [Demo Script](#demo-script)
- [Implementation Roadmap](#implementation-roadmap)
- [Security](#security-best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Diligence** is a prototype pipeline for:

1. **Extracting falsifiable claims** from PDF investment decks and pitches
2. **Verifying claims** using multiple methods:
   - Heuristic pattern matching
   - EDGAR financial data search
   - AI model-based verification (Gemini)
3. **Generating investment memos** with confidence scores and verification status

### Key Features

✅ **End-to-end pipeline** — Extract → Verify → Memo  
✅ **Graceful fallback** — Works with or without AI models  
✅ **Model flexibility** — Supports Gemini API or custom HTTP endpoints  
✅ **Open source** — Python, easy to integrate into other tools  
✅ **Benchmarked** — Includes 5-deck labeled dataset for evaluation  

### Tech Stack

- **Language:** Python 3
- **PDF Processing:** pypdf
- **Data Validation:** jsonschema
- **Model Integration:** Gemini API, Google Vertex AI
- **Financial Data:** SEC EDGAR API (optional)
- **CI/CD:** GitHub Actions

---

## Quick Start

### Heuristic Extraction (No API Key Required)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add PDF decks:** Put 2–3 PDF decks in `demo/inputs/`

3. **Run full pipeline:**
   ```bash
   python run_pipeline.py
   ```

4. **Inspect outputs** in `demo/outputs/`:
   - `claims.json` — Extracted claims
   - `claims_checked.json` — Verified claims
   - `questions.md` — Unverifiable claims as founder questions
   - `memo.md` — Investment memo

### With Gemini API (Recommended)

1. **Get API key:** https://makersuite.google.com/app/apikeys

2. **Create `.env` file:**
   ```bash
   MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
   GEMINI_API_KEY=your-api-key-here
   ```

3. **Run:** `python run_pipeline.py`

---

## Model-Backed Extraction (Recommended)

### Why Use Models?

- **Higher recall:** +15-25% improvement over heuristics
- **Better context:** Captures nuanced claims
- **Automated verification:** Cross-references with sources

### Setup (2 minutes)

1. Get free API key at https://makersuite.google.com/app/apikeys
2. Add to `.env`:
   ```bash
   MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
   GEMINI_API_KEY=AIzaSyC_mG4F5vK3xH9jZ7q2w8x1y5z4a3b6c7d8e9f0g1h2i3j4k5l6m7n8o
   ```
3. Run: `python run_pipeline.py`

### Model Options

| Model | Speed | Accuracy | Cost |
|-------|-------|----------|------|
| gemini-1.5-flash | Fast | Good | Free tier |
| gemini-1.5-pro | Slower | Excellent | Paid |

**Cost:** Free tier = 15 req/min, 1500/day. Paid = ~1¢ per 5-page deck.

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  EXTRACT    │ ──▶ │   VERIFY     │ ──▶ │    MEMO     │
│             │     │              │     │             │
│ • Heuristic │     │ • Patterns   │     │ • Markdown  │
│ • Model API │     │ • EDGAR      │     │ • Sources   │
│             │     │ • Model API  │     │ • Scores    │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Stage 1: Extract
- Heuristic analysis (always available)
- Gemini model (when configured)
- Output: `claims.json` with claim, source_file, page, type

### Stage 2: Verify
- Pattern matching
- EDGAR search (optional)
- Model verification
- Output: `claims_checked.json` with status, confidence, evidence

### Stage 3: Memo
- Verified claims with sources
- Confidence scores
- Questions for founders
- Output: `memo.md`

### Fallback Strategy
Without API keys:
- Extraction → heuristic PDF analysis
- Verification → regex patterns
- Pipeline always produces output

---

## Commands

| Command | Description |
|---------|-------------|
| `python run_pipeline.py` | Full pipeline |
| `python run_pipeline.py --step 1` | Extract only |
| `python run_pipeline.py --step 2` | Verify only |
| `python run_pipeline.py --step 3` | Memo only |
| `python bench.py bench/` | Run benchmark |

---

## Configuration Reference

All via `.env` file. All optional; defaults used if not set.

### Core

| Variable | Purpose | Default |
|----------|---------|---------|
| `MODEL_API_URL` | Gemini endpoint | gemini-1.5-flash |
| `GEMINI_API_KEY` | API key | Not set |
| `ENABLE_MODEL_VERIFICATION` | Use model verification | 1 |

### Model Parameters

| Variable | Purpose | Default |
|----------|---------|---------|
| `MODEL_VERIFIER_BATCH_SIZE` | Claims per batch | 5 |
| `MODEL_VERIFIER_TEMPERATURE` | Creativity (0-1) | 0.1 |
| `MODEL_VERIFIER_MAX_TOKENS` | Max response tokens | 512 |

### GCP/Vertex AI (Optional)

| Variable | Purpose | Default |
|----------|---------|---------|
| `GCP_PROJECT_ID` | Google Cloud project | cent-capital-472820 |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account path | (not used) |
| `GCP_REGION` | Vertex region | us-central1 |
| `GEMINI_MODEL` | Vertex model name | gemini-1.5-flash |

### Extraction

| Variable | Purpose | Default |
|----------|---------|---------|
| `EXTRACTION_CONFIDENCE_THRESHOLD` | Min confidence (0-1) | 0.3 |
| `EXTRACTION_MIN_TOKENS_PER_CLAIM` | Min tokens per claim | 5 |

### EDGAR (Optional)

| Variable | Purpose | Default |
|----------|---------|---------|
| `USE_EDGAR` | Enable EDGAR | 0 |
| `SEC_USER_AGENT` | SEC API user agent | Not set |

### Confidence Thresholds

| Variable | Purpose | Default |
|----------|---------|---------|
| `VERIFICATION_HIGH_CONFIDENCE_THRESHOLD` | High threshold | 0.9 |
| `VERIFICATION_MEDIUM_CONFIDENCE_THRESHOLD` | Medium threshold | 0.6 |
| `VERIFICATION_LOW_CONFIDENCE_THRESHOLD` | Low threshold | 0.3 |

### Memo

| Variable | Purpose | Default |
|----------|---------|---------|
| `MEMO_INCLUDE_SOURCES` | Include sources | 1 |
| `MEMO_INCLUDE_CONFIDENCE_SCORES` | Include scores | 1 |
| `MEMO_SORT_BY_CONFIDENCE` | Sort by confidence | 1 |

### Debug

| Variable | Purpose | Default |
|----------|---------|---------|
| `DEBUG` | Verbose logging | 0 |
| `LOG_FILE` | Log file path | (not set) |

### Examples

**Minimal (heuristics):** No config needed

**Standard (Gemini):**
```bash
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=YOUR_KEY
```

**High-Accuracy:**
```bash
MODEL_API_URL=...gemini-1.5-pro:generateContent
GEMINI_API_KEY=YOUR_KEY
MODEL_VERIFIER_TEMPERATURE=0.05
USE_EDGAR=1
```

**Debug:**
```bash
DEBUG=1
LOG_FILE=logs/diligence.log
```

### Loading Priority
CLI > Environment > .env > Defaults

---

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
├── demo/                    # Sample inputs/outputs
├── bench/                   # Labeled dataset
└── docs/                    # Documentation
```

---

## Performance & Benchmarking

### Results (5-deck dataset)

| Method | Precision | Recall |
|--------|-----------|--------|
| Heuristic-only | 0.90 | 0.60 |
| Gemini API | ~0.90 | ~0.75-0.85 |

**Note:** Five decks is five decks. Sample size limited but honestly reported.

### Run Benchmark
```bash
python bench.py bench/
```

---

## Use Cases

- **Due diligence teams** — Automate claim extraction
- **Investors** — Verify claims quickly
- **Analysts** — Generate structured reports
- **Research** — Claim extraction/verification benchmark

---

## Demo Script

**10-minute flow:**

| Min | Beat |
| --- | --- |
| 1 | Show the folder: "A real deal, assembled in five minutes." |
| 2 | Run extract live. Claims appear with page numbers. |
| 2 | Open `questions.md`: "Everything unconfirmed becomes my founder call agenda." |
| 2 | Show memo. Trace one number to its source page. |
| 1 | Show benchmark. Volunteer sample-size caveat. |
| 2 | Close: "The model does not make the call. Provenance exists so I can defend every number." |

### Two Keys to Success

1. **Volunteer failure modes.** Show a wrong claim before being asked.
2. **Don't oversell accuracy.** Five decks is five decks. Say so.

---

## Implementation Roadmap

### Session 1 — End-to-End (3 hrs) ✅
- [x] Gemini Flash file upload, single call
- [x] Response schema: claim, source_file, page, type
- [x] Write claims.json

### Session 2 — Verify (3 hrs) ✅
- [x] verify() reads claims.json
- [x] EDGAR search
- [x] Model sorts: verified/contradicted/unverifiable
- [x] Write claims_checked.json, questions.md

### Session 3 — Memo, Benchmark (4 hrs) ✅
- [x] memo() with sources, kill signals
- [x] Run on ProbeTruth
- [x] 5-deck benchmark
- [x] bench.py reports precision/recall

### Session 4 — Demoable (2 hrs) ✅
- [x] README
- [x] demo/ folder
- [x] --step flag

### Cut Without Hesitation
Reference-call transcription · incremental reruns · UI · extensive tests · founder-answer loop

---

## Security Best Practices

### ✅ DO:
- Store API keys in `.env` (in .gitignore)
- Use GitHub Secrets in CI/CD
- Rotate keys periodically
- Use minimal permissions

### ❌ DON'T:
- Commit `.env` to git
- Share keys in PRs/issues
- Use same key for dev/prod
- Store keys in tracked files

---

## Troubleshooting

### Configuration

| Issue | Solution |
|-------|----------|
| `.env` changes don't apply | Reload terminal/IDE |
| "Model extractor not configured" | Set MODEL_API_URL and GEMINI_API_KEY |
| Still using heuristics | Reload after updating .env |

### API Key

| Issue | Solution |
|-------|----------|
| "401 Unauthorized" | Verify key from AI Studio |
| "Resource not found" | Check MODEL_API_URL exactly |
| "Rate limit exceeded" | Wait 1-2 min (free: 15 req/min) |

### Getting Help
1. Check `.env` exists and formatted correctly
2. Verify key starts with `AIza`
3. No spaces/extra characters
4. Try fresh key from https://makersuite.google.com/app/apikeys

---

## Contributing

Prototype project. Fork and adapt.

### Improvement Areas
- Fine-tune heuristics
- Expand labeled dataset
- Add Claude/LLaMA support
- Implement EDGAR integration
- Add web UI

### Adding Configuration
1. Add to `.env.example` with comment
2. Add to `.env` with placeholder
3. Reference in code: `os.environ.get('VAR', 'default')`
4. Document here
5. Test with/without variable

---

## Additional Resources

- **Repository:** https://github.com/beastofbayarea/diligence
- **Gemini Setup:** `GEMINI_API_SETUP.md`
- **Implementation Plan:** `IMPLEMENTATION_PLAN.md`
- **Config Reference:** `CONFIG_REFERENCE.md`
- **Repo Info:** `REPOSITORY_INFO.md`

---

## License

Not specified (check repo)

---

## Contact

**GitHub:** @beastofbayarea  
**Repository:** https://github.com/beastofbayarea/diligence

---

**Last Updated:** 2026-08-05  
**Status:** Production-ready prototype with fallback strategy

---

## Quick Start Summary

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure (recommended)
echo "MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent" > .env
echo "GEMINI_API_KEY=YOUR_KEY_HERE" >> .env

# 3. Run
python run_pipeline.py

# 4. Check outputs
ls demo/outputs/
```

**Your API key activates model-backed extraction.** Get it in 1 minute from [Google AI Studio](https://makersuite.google.com/app/apikeys), update `.env`, and run.
