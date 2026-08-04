# diligence

Turns a deal folder into an IC memo. Three Gemini Flash calls, no framework.

```bash
python diligence.py --folder <drive-folder-id>
```

## What it does

```
Drive folder  →  extract()  →  claims.json
                 verify()   →  claims_checked.json + questions.md
                 memo()     →  memo.md
```

`extract` reads every PDF and pulls out each falsifiable claim with its source and page.
`verify` cross-checks those claims against SEC EDGAR and sorts them: **asserted**, **verified**, **unverifiable**.
`memo` writes the IC memo, every number carrying a source tag and every risk a named kill signal.

The unverifiable list is the point. It becomes `questions.md` — the agenda for the founder call.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env    # add GEMINI_API_KEY
python auth.py          # one-time Google OAuth consent
```

## The deal folder

Flat, one folder per deal, in Drive. Anything in it gets read.

| | |
|---|---|
| From the founder | deck, model, cap table, term sheet, customer contracts |
| From the public record | founder LinkedIn PDFs, site and pricing, news, patents, job postings |
| From you | `context.md` |

`context.md` is three or four sentences: how the deal came in, who the proposed lead is,
round size and stage, what you already believe, what worries you. Write it before you run
anything — it is the pre-registration step, and it stops the output reading as confirmation.

Google Docs and Sheets are exported to PDF on fetch. Shared drives work.

## Rerunning

After the founder call, append their answers to `context.md` and run `verify` again.
Claims move from unverifiable to verified or contradicted. This second pass is where
the workflow earns its keep.

```bash
python diligence.py --folder <id> --step verify
```

## Accuracy

`bench/` holds 20 decks with hand-labelled ground truth.

```bash
python bench.py
```

Reports precision and recall on claim extraction. Run it before trusting a memo.

## Cost

A few dollars per deal in tokens. Everything else is free tier or open source.

## Notes

Confirm where your API calls are processed before pointing this at a data room under NDA.

The model does not make the recommendation. You do. Provenance tags exist so every
number in the memo can be traced and defended out loud.
