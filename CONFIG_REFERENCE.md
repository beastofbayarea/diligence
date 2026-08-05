# Configuration Reference

## .env File Variables

The `.env` file controls how the diligence pipeline behaves. All variables are optional; if not set, defaults are used.

### Gemini API Configuration (Recommended)

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MODEL_API_URL` | HTTP endpoint for Gemini model | `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent` | gemini-1.5-flash |
| `GEMINI_API_KEY` | Authentication key for Gemini API | Your API key from Google AI Studio | Not set |
| `ENABLE_MODEL_VERIFICATION` | Use model for claim verification | `1` | 1 |

### Model Verification Parameters

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MODEL_VERIFIER_BATCH_SIZE` | Claims to verify in one batch | `5` | 5 |
| `MODEL_VERIFIER_TEMPERATURE` | Model response creativity (0-1) | `0.1` (deterministic) | 0.1 |
| `MODEL_VERIFIER_MAX_TOKENS` | Max tokens in verification response | `512` | 512 |

### GCP / Vertex AI Configuration (Optional)

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `GCP_PROJECT_ID` | Google Cloud project ID | `cent-capital-472820` | cent-capital-472820 |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON | `gemini-service-account.json` | (not used) |
| `GCP_REGION` | Vertex AI region | `us-central1` | us-central1 |
| `GEMINI_MODEL` | Model name in Vertex | `gemini-1.5-flash` | gemini-1.5-flash |

### PDF Extraction Configuration

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `EXTRACTION_CONFIDENCE_THRESHOLD` | Minimum confidence for claims (0-1) | `0.3` | 0.3 |
| `EXTRACTION_MIN_TOKENS_PER_CLAIM` | Minimum tokens in extracted claim | `5` | 5 |

### EDGAR Verification (Optional)

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `USE_EDGAR` | Enable EDGAR financial verification | `1` | 0 |
| `SEC_USER_AGENT` | User agent for SEC API | `DiligenceApp/1.0 (you@example.com)` | Not set |

### Verification Confidence Thresholds

| Variable | Purpose | Range | Default |
|----------|---------|-------|---------|
| `VERIFICATION_HIGH_CONFIDENCE_THRESHOLD` | High confidence threshold | 0-1 | 0.9 |
| `VERIFICATION_MEDIUM_CONFIDENCE_THRESHOLD` | Medium confidence threshold | 0-1 | 0.6 |
| `VERIFICATION_LOW_CONFIDENCE_THRESHOLD` | Low confidence threshold | 0-1 | 0.3 |

### Memo Generation Configuration

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MEMO_INCLUDE_SOURCES` | Include source files in memo | `1` | 1 |
| `MEMO_INCLUDE_CONFIDENCE_SCORES` | Include confidence scores | `1` | 1 |
| `MEMO_SORT_BY_CONFIDENCE` | Sort claims by confidence score | `1` | 1 |

### Logging & Debug

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `DEBUG` | Enable verbose logging | `1` (verbose) | 0 |
| `LOG_FILE` | Write logs to file | `logs/diligence.log` | (not set) |

## Configuration Examples

### Minimal Configuration (Heuristics Only)

```bash
# .env
# Only install dependencies and run:
python run_pipeline.py
# No configuration needed for heuristic extraction
```

### Standard Configuration (With Gemini API)

```bash
# .env
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=AIzaSyC_mG4F5vK3xH9jZ7q2w8x1y5z4a3b6c7d8e9f0g1h2i3j4k5l6m7n8o

# Now run:
python run_pipeline.py
```

### High-Accuracy Configuration (Gemini Pro + EDGAR)

```bash
# .env
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
GEMINI_API_KEY=YOUR_API_KEY

MODEL_VERIFIER_TEMPERATURE=0.05
MODEL_VERIFIER_MAX_TOKENS=768

USE_EDGAR=1
SEC_USER_AGENT=DiligenceApp/1.0 (your-email@example.com)

MEMO_INCLUDE_CONFIDENCE_SCORES=1
MEMO_SORT_BY_CONFIDENCE=1
```

### Development Configuration (With Debug Logging)

```bash
# .env
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=YOUR_API_KEY

DEBUG=1
LOG_FILE=logs/diligence.log

EXTRACTION_CONFIDENCE_THRESHOLD=0.2
MODEL_VERIFIER_BATCH_SIZE=2
```

## How Configuration is Loaded

1. **Defaults** — Built-in defaults are used
2. **Environment Variables** — Override defaults (set via shell)
3. **.env File** — Loaded automatically by `env_loader.py` at startup
4. **CLI Arguments** — (Not currently supported, but could be added)

Priority: CLI > Environment > .env > Defaults

## Secure Configuration

### ✅ DO:
- Store API keys in `.env` file (it's in `.gitignore`)
- Use environment variables in CI/CD (GitHub Secrets)
- Rotate API keys periodically
- Use minimal permissions for service accounts

### ❌ DON'T:
- Commit `.env` to git
- Share API keys in pull requests or issues
- Use the same key for dev and production
- Store keys in `.env.example` or other tracked files

## Troubleshooting

### Configuration Not Loading

**Problem:** Changes to `.env` don't take effect

**Solution:**
1. Reload your terminal/IDE
2. Check `.env` is in the repo root
3. Verify `env_loader.py` is imported in your script
4. Try exporting variables manually: `$env:GEMINI_API_KEY = "..."`

### Missing Configuration

**Problem:** "Model extractor not configured"

**Solution:** Set both `MODEL_API_URL` and `GEMINI_API_KEY`:
```bash
# In .env:
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=YOUR_API_KEY
```

### API Key Not Working

**Problem:** "401 Unauthorized" or "UNAUTHENTICATED"

**Solution:**
1. Get a fresh API key from https://makersuite.google.com/app/apikeys
2. Verify it starts with `AIza`
3. Check it's copied completely (no spaces)
4. Verify the key is enabled in Google Cloud

## Adding New Configuration

To add a new `.env` variable to the pipeline:

1. Add it to `.env.example` with a comment
2. Add it to `.env` with a placeholder
3. Reference it in your code: `os.environ.get('VARIABLE_NAME', 'default_value')`
4. Document it here in `CONFIG_REFERENCE.md`
5. Test it works with and without the variable set

## Next Steps

- Copy `.env.example` to `.env`
- Add your Gemini API key
- Run `python run_pipeline.py`
- Inspect `demo/outputs/` for results
