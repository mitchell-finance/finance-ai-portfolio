# Which hourly rate can finance use?

A signed amendment puts installation up to £83. A surveyor works on the same project on the same day. Does their rate change too? I built this small pilot to see whether a model could find the applicable clause, respect the phase and work date, and refer an unresolved file to a colleague.

I wrote eight short fictional files and an answer key under a single desk policy. I submitted the [policy and case text](prompt.txt) together in a fresh read-only Codex session using OpenAI gpt-6-astra on 26 November 2026. The prompt contained no answer key. I saved the [response](observed.json) and compared it with the [reference decisions](reference.json).

| Measure | Observed in one run |
| --- | --- |
| Rate on the five cases with a supportable price | 5 of 5 correct |
| Referral on the three cases requiring a person | 3 of 3 referred |
| Required clause IDs present, with no invented or cross-case ID | 8 of 8 |
| Rate suggested on a case requiring referral | 0 of 3 |

Case D turns on one day. Both sides have already signed the increase to £90, but the work took place the day before it applied. The answer was £71. In case G the increase depends on handover and the handover date is missing. I would ask the project manager for the dated handover record before billing.

## Replay the evaluation

From this folder, run `python evaluate.py`. To try another model, give it the complete contents of `prompt.txt` in a fresh session, save its JSON response and run `python evaluate.py path/to/answer.json`. The evaluator reports each decision and its source coverage separately. Extra same-case citations are permitted. A source ID check cannot judge the quality of an explanation.

These are eight purpose-written cases, one model run and a reference key prepared for the exercise. The files contain short transcribed clauses. Before relying on this for billing I would test complete unseen packs, including scans and missing schedules, against decisions recorded independently by a commercial reviewer. Every suggested rate here is for review. Nothing is posted to a ledger.

[Back to the portfolio](../../README.md)
