# Gemini API Setup — 3 Minutes to Model-Backed Extraction

## Step 1: Get API Key (1 minute)
Open: https://makersuite.google.com/app/apikeys
Click: **"Create API Key"**
Copy: The generated key

## Step 2: Create .env File (1 minute)
Create a file named `.env` in the repo root with:

```
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
GEMINI_API_KEY=paste-your-api-key-here
```

## Step 3: Run Pipeline (1 minute)
```bash
python run_pipeline.py
```

The pipeline will now use Gemini to extract and verify claims!

---

## What You Get

✅ **Better accuracy** — Model-backed extraction vs heuristics  
✅ **Automatic verification** — Claims verified against Gemini  
✅ **Fallback support** — Heuristics kick in if model unavailable  
✅ **Free tier** — 15 requests/min, 1500 requests/day  

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Model extractor not configured" | Check .env file created & `GEMINI_API_KEY` set |
| "401 Unauthorized" | Verify API key is correct from AI Studio |
| "Rate limit exceeded" | Wait 1 minute, then retry |
| Still using heuristics | Reload terminal after creating .env |

## Optional: Use Faster Free Model

For fastest responses (lowest latency), use flash:
```
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

For highest accuracy (slower), use pro:
```
MODEL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
```

## Next

Run: `python run_pipeline.py`  
Output: Check `demo/outputs/` for results  
Benchmark: `python bench.py bench/`
