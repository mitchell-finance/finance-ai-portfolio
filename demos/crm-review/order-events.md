# A PO arrives twice. How much of the deal is actually covered?

I built this example with sample verified order events for a £48,000 opportunity. The feed first delivers a £16,000 revision, then the superseded £12,000 original, then a duplicate of the revision. A £32,000 order also arrives for another opportunity.

**I’d report £16,000 covered and keep £32,000 open.** Counting every notification inflates the forecast. Taking the last arrival as current can also roll a deal back. I match the opportunity and order, keep the highest verified revision and flag contradictory versions for investigation.

Run `python order_events.py` and `python -m unittest -v test_order_events`. [Inspect the event stream](order_events.py). Revisions contain the full replacement order value. A zero-value newer revision represents cancellation. Order cover here means verified commitments in one currency; revenue recognition is a separate decision.

AI can suggest the opportunity from the meeting notes. The calculation requires a confirmed opportunity match and verified source events. Sales reviews the remaining forecast before updating the CRM.

[Back to CRM review](README.md)
