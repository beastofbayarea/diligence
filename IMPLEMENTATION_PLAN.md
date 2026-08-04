# Implementation plan — diligence prototype

**Goal:** a working prototype demoable in ten minutes that survives follow-up questions.
**Budget:** ~12 hours across two evenings and one weekend day.
**Constraint:** build backwards from the demo, not forwards from the architecture.

---

## Session 1 — One call, end to end (3 hrs)

No Drive, no auth, no CLI. Three PDFs in a local folder.

- [ ] Gemini Flash file upload, two or three PDFs in a **single call**
- [ ] Response schema returning `claim`, `source_file`, `page`, `type`
- [ ] Print the claims table to console
- [ ] Write `claims.json`

**Force JSON with a response schema, not a prompt instruction.** Parsing free-text JSON
failures will eat the entire evening otherwise.

> **Done when:** you point at a real deck and see ~30 extracted claims with page numbers.
> That alone is demoable.

---

## Session 2 — Verify (3 hrs)

The interesting half. Extraction is table stakes; honest sorting of what you cannot
confirm is not.

- [ ] `verify()` reads `claims.json`
- [ ] EDGAR full-text search for the company and the proposed lead
- [ ] Second Flash call sorts each claim: **verified / contradicted / unverifiable**
- [ ] Write `claims_checked.json`
- [ ] Write `questions.md` from the unverifiable rows

> **Done when:** `questions.md` reads like a founder call agenda you would actually use.

---

## Session 3 — Memo, benchmark, one real deal (4 hrs)

- [ ] `memo()` produces markdown with source tags and named kill signals
- [ ] Run the full pipeline on **ProbeTruth**, compare against the manual memo
- [ ] Benchmark: **5 decks, hand-labelled** — not 20
- [ ] `bench.py` reports precision and recall on claim extraction

Five labelled decks is enough to state a number honestly and caveat the sample size.
Twenty is a week you do not have.

> **Done when:** you can say a precision number out loud and defend how you got it.

---

## Session 4 — Make it demoable (2 hrs)

- [ ] README
- [ ] `demo/` folder with the committed ProbeTruth run: inputs, all three outputs, console log
- [ ] `--step` flag so any stage reruns live without redoing the pipeline

**Add Drive only if time remains.** It is the piece most likely to burn two hours on OAuth
scopes and shared-drive flags, and it adds nothing to the demo narrative.

---

## Cut without hesitation

Reference-call transcription · incremental reruns · a UI · error handling beyond
try/except · tests · the founder-answer loop.

Mention all of them as roadmap. Building any of them costs demo polish better spent
elsewhere.

---

## Demo script — ten minutes

| Min | Beat |
|---|---|
| 1 | **Show the folder.** "A real deal, assembled in five minutes." |
| 2 | **Run extract live.** Claims appear with page numbers. |
| 2 | **Open `questions.md`.** "This is the part I care about — everything the model could not confirm becomes my founder call agenda." |
| 2 | **Show the memo.** Trace one number back to its source page. |
| 1 | **Show the benchmark.** Volunteer the sample-size caveat before they ask. |
| 2 | **Close on the limitation.** "The model does not make the call. Provenance exists so I can defend every number in the room." |

---

## The two things that decide whether this lands

**Volunteer the failure modes.** Show a claim the extractor got wrong. A candidate who
demos their tool's error before being asked reads as someone who runs real diligence.
A flawless demo reads as a cherry-picked one.

**Do not oversell the accuracy number.** Five decks is five decks. Say so.
