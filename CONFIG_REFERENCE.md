# Configuration Reference — Diligence Pipeline & Streamlit UI

The `.env` file controls how the **Diligence** pipeline, model extractors, financial data verifiers, and Streamlit web application behave. All variables are optional; if not set, sensible defaults and heuristic fallbacks are used automatically.

---

## Environment Variables Summary

### 1. Gemini & AI Model Configuration (Recommended)

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MODEL_API_URL` | HTTP endpoint for Gemini model API | `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent` | `gemini-1.5-flash` |
| `GEMINI_API_KEY` | Authentication API key from Google AI Studio | `AIzaSy...` | Not set |
| `ENABLE_MODEL_VERIFICATION` | Enable AI-backed claim verification | `1` (enabled) / `0` (disabled) | `1` |
| `OPENROUTER_API_KEY` | OpenRouter multi-provider API key | `sk-or-v1-...` | Not set |
| `GROK_API_KEY` | xAI Grok platform API key | `xai-...` | Not set |

---

### 2. Model Verification Parameters

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MODEL_VERIFIER_BATCH_SIZE` | Number of claims to send in a single batch | `5` | `5` |
| `MODEL_VERIFIER_TEMPERATURE` | Creativity/determinism setting (0.0 - 1.0) | `0.1` | `0.1` |
| `MODEL_VERIFIER_MAX_TOKENS` | Maximum tokens returned per verification batch | `512` | `512` |

---

### 3. Financial & Market Data APIs

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `FMP_API_KEY` | Financial Modeling Prep API key for profile & statement verification | `caOlFmal...` | Not set |
| `USE_EDGAR` | Enable SEC EDGAR full-text search verification | `1` (enabled) / `0` (disabled) | `1` |
| `SEC_USER_AGENT` | Required User-Agent header for SEC API compliance | `DiligenceApp/1.0 (shiv@cent.capital)` | Default string |
| `FRED_API_KEY` | Federal Reserve Economic Data API key | `5a4a1a...` | Not set |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage financial API key | `IHY98VQ...` | Not set |

---

### 4. GCP / Vertex AI Configuration (Optional)

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `GCP_PROJECT_ID` | Google Cloud project ID for Vertex AI | `cent-capital-472820` | `cent-capital-472820` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON file | `C:\Users\...\credentials.json` | Not set |
| `GCP_REGION` | Vertex AI regional endpoint | `us-central1` or `global` | `us-central1` |
| `GEMINI_MODEL` | Gemini model ID in Vertex AI | `gemini-flash-latest` | `gemini-1.5-flash` |

---

### 5. Verification Confidence & Extraction Thresholds

| Variable | Purpose | Range | Default |
|----------|---------|-------|---------|
| `EXTRACTION_CONFIDENCE_THRESHOLD` | Heuristic extraction score threshold | 0.0 - 1.0 | `0.3` |
| `EXTRACTION_MIN_TOKENS_PER_CLAIM` | Minimum token length for extracted claims | > 0 | `5` |
| `VERIFICATION_HIGH_CONFIDENCE_THRESHOLD` | High confidence score cut-off | 0.0 - 1.0 | `0.9` |
| `VERIFICATION_MEDIUM_CONFIDENCE_THRESHOLD` | Medium confidence score cut-off | 0.0 - 1.0 | `0.6` |
| `VERIFICATION_LOW_CONFIDENCE_THRESHOLD` | Low confidence score cut-off | 0.0 - 1.0 | `0.3` |

---

### 6. Memo Generation & Logging

| Variable | Purpose | Example | Default |
|----------|---------|---------|---------|
| `MEMO_INCLUDE_SOURCES` | Include source document and page number in memo | `1` | `1` |
| `MEMO_INCLUDE_CONFIDENCE_SCORES` | Render confidence ratings in memo markdown | `1` | `1` |
| `MEMO_SORT_BY_CONFIDENCE` | Sort verified claims by confidence score | `1` | `1` |
| `DEBUG` | Enable verbose console output | `1` | `0` |
| `LOG_FILE` | Optional path to write log output | `logs/diligence.log` | Not set |

---

## Configuration Setup Examples

### Standard Setup (.env file)

```bash
# Model & Verification
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=your-gemini-api-key-here
ENABLE_MODEL_VERIFICATION=1

# Financial Verification APIs
FMP_API_KEY=your-fmp-api-key-here
USE_EDGAR=1
SEC_USER_AGENT=DiligenceApp/1.0 (shiv@cent.capital)
```

---

## How Environment Variables Are Loaded

1. **Auto-Load**: `env_loader.py` automatically reads `.env` on script start.
2. **Override Order**: Shell Environment Variables > `.env` file > Built-in Defaults.
3. **Streamlit UI Integration**: Settings tab in `app.py` allows updating API keys live during execution.
