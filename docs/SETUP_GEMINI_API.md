# Setup Guide: Gemini API for Model-Backed Extraction & Verification

This guide explains how to configure the diligence pipeline to use Google's Gemini API for model-backed claim extraction and verification.

## Quick Start (Recommended)

### Step 1: Get a Gemini API Key

1. Open **Google AI Studio**: https://makersuite.google.com/app/apikeys
2. Click **"Create API Key"** (free tier available)
3. Copy the generated API key

### Step 2: Create `.env` file

Create a `.env` file in the repo root with:

```bash
# Gemini API configuration (for HTTP model-backed extraction)
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=your-api-key-here
```

**Replace `your-api-key-here` with your actual API key.**

### Step 3: Run the pipeline with model-backed extraction

```bash
python run_pipeline.py
```

The pipeline will now:
1. Use Gemini to extract claims from PDFs
2. Validate claims against the response schema
3. Fall back to heuristics if model calls fail

## Alternative Models

If you prefer a different Gemini model, use one of these endpoints:

```bash
# Fast, efficient model (recommended)
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent

# More powerful model (slower, higher accuracy)
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent

# Latest available model
https://generativelanguage.googleapis.com/v1beta/models/gemini-latest:generateContent
```

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `MODEL_API_URL` | HTTP endpoint for model API | `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent` |
| `GEMINI_API_KEY` | API authentication key | (from Google AI Studio) |
| `GCP_PROJECT_ID` | GCP project (optional, for Vertex) | `cent-capital` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account path (optional, for Vertex) | `service-account-key.json` |

## Verification with Model-Backed Verifier

Once `GEMINI_API_KEY` is configured, the pipeline's verification stage will use Gemini to verify claims in addition to heuristics and EDGAR search:

1. **Stage 2** reads extracted claims
2. Attempts verification via:
   - Heuristics (regex patterns)
   - EDGAR search (if `USE_EDGAR=1` is set)
   - **Gemini model verification** (if `GEMINI_API_KEY` is set)
3. Writes verified results to `demo/outputs/claims_checked.json`

## Cost & Rate Limits

- **Free tier**: 15 requests/minute, 1500 requests/day (Gemini 1.5 Flash)
- **Paid**: More generous limits with billing account
- See https://ai.google.dev/pricing for details

## Troubleshooting

### "Model extractor not configured"
- Ensure both `MODEL_API_URL` and `GEMINI_API_KEY` are set in `.env` or environment
- Reload the terminal after creating `.env`

### "Model returned JSON that does not match expected schema"
- The model response format may have changed; check logs for response structure
- File an issue with the model output for debugging

### API Key rejected / 401 Unauthorized
- Verify the API key is correct and enabled for Generative Language API
- Check https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com

### Rate limit exceeded
- Wait a few minutes and retry
- Consider upgrading to paid tier for higher limits

## Next Steps

1. Get your API key: https://makersuite.google.com/app/apikeys
2. Create `.env` with `MODEL_API_URL` and `GEMINI_API_KEY`
3. Run `python run_pipeline.py` to execute with model-backed extraction
4. Run `python bench.py bench/` to evaluate precision/recall

## Security Notes

- **Never commit `.env` to git** — it's in `.gitignore`
- Do not share your API key; treat it like a password
- Rotate keys periodically in Google AI Studio
- For CI/CD, use GitHub Secrets or GCP secrets manager
