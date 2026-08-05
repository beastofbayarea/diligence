# Gemini API Setup — Get Model-Backed Extraction Working in 2 Minutes

## Current Status

✅ **Heuristic extraction is working** — pipeline runs with fallback logic  
✅ **.env file created** — ready for API key  
✅ **Gemini service account available** — for Vertex AI (if IAM permits)  
⏳ **Waiting for:** Gemini API key to enable model-backed extraction

## Quick Setup (Recommended Path)

### Step 1: Get a Free Gemini API Key (1 minute)

1. Open **Google AI Studio**: https://makersuite.google.com/app/apikeys
2. Click **"Create API Key"** button
3. Copy the generated API key
4. **Note:** Free tier includes 15 requests/min, 1500 requests/day

### Step 2: Add API Key to .env (30 seconds)

The `.env` file already exists in the repo root. Edit it:

```bash
# Open .env and replace PASTE_YOUR_API_KEY_HERE with your actual key:
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
```

**Example:**
```bash
GEMINI_API_KEY=AIzaSyC_mG4F5vK3xH9jZ7q2w8x1y5z4a3b6c7d8e9f0g1h2i3j4k5l6m7n8o
```

### Step 3: Run Pipeline (30 seconds)

```bash
python run_pipeline.py
```

That's it! The pipeline will now use Gemini for claim extraction and verification.

## Verify It Works

After running `python run_pipeline.py`, check:
- `demo/outputs/claims.json` — should have extracted claims
- `demo/outputs/claims_checked.json` — should have verification results
- `demo/outputs/memo.md` — investment memo

## Optional: Choose a Different Model

The free tier uses `gemini-1.5-flash` (faster). To use `gemini-1.5-pro` (more accurate but slower):

```bash
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
GEMINI_API_KEY=YOUR_API_KEY
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model extractor not configured" | Check `.env` file exists and `GEMINI_API_KEY` is set |
| "401 Unauthorized" or "UNAUTHENTICATED" | Verify API key is correct (copy-paste from AI Studio) |
| "Resource not found" | Check `MODEL_API_URL` is exactly as shown above |
| "Rate limit exceeded" | Wait 1-2 minutes, then retry (free tier: 15 req/min) |
| Pipeline still using heuristics | Reload terminal/IDE after updating `.env` |

## Cost Breakdown

- **Free tier:** 15 requests/min, 1500 requests/day (enough for demos)
- **Paid tier:** $0.075/million input tokens, $0.30/million output tokens
- **Estimated cost:** ~1¢ per 5-page deck with model-backed extraction

See [pricing](https://ai.google.dev/pricing) for details.

## Environment Variables Reference

After `.env` is configured, the pipeline automatically loads these:

| Variable | What It Does |
|----------|--------------|
| `MODEL_API_URL` | HTTP endpoint for Gemini model |
| `GEMINI_API_KEY` | API key for authentication |
| `GCP_PROJECT_ID` | GCP project ID (for Vertex fallback) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account (for Vertex fallback) |
| `GCP_REGION` | GCP region (for Vertex) |
| `GEMINI_MODEL` | Model name in Vertex (for Vertex) |

## Security Notes

- **Never commit `.env` to git** — it's in `.gitignore`
- **Treat your API key like a password** — don't share it
- **Rotate keys periodically** in Google AI Studio
- **For CI/CD:** Use GitHub Secrets, not `.env` files

## Next Steps

1. **Get API key**: https://makersuite.google.com/app/apikeys (takes 30 seconds)
2. **Update `.env`** with your key
3. **Run**: `python run_pipeline.py`
4. **Benchmark**: `python bench.py bench/`

## Additional Resources

- Setup detailed guide: `docs/SETUP_GEMINI_API.md`
- Implementation status: `docs/IMPLEMENTATION_STATUS.md`
- Quick start: `docs/QUICK_START_GEMINI.md`
- Main README: `README.md`

---

**Your API key is the only thing needed to activate model-backed extraction.** Get it in 1 minute from [Google AI Studio](https://makersuite.google.com/app/apikeys), then update `.env` and run the pipeline.
