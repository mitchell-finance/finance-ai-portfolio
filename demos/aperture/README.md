# Aperture: can I still match this invoice after an inspection correction?

I built and directed Aperture for procurement and accounts payable. In the recorded development walkthrough I demonstrated approval against a specific order version and a receiving history that retains the original inspection when someone corrects the accepted quantity.

I built this independent example with sample records to show how those two controls affect a finance decision.

| Evidence | First review | After reinspection |
| --- | ---: | ---: |
| Delivered | 60 units | 60 units |
| Accepted to date | 48 | 36 |
| Already billed | 12 | 12 |
| Remaining accepted units | **36** | **24** |

The new invoice is for 36 units. It initially matches. After reinspection it exceeds the available quantity by 12. I’d hold the invoice and ask receiving to confirm the correction. At £45 per unit, £540 needs resolving. If the order itself has changed, approval for the old revision also fails the check.

Run `python receipt_review.py` and `python -m unittest -v` from this directory. Inspection revisions are cumulative and can arrive out of order. The public replay covers one line, assumes the recorded order price and takes prior billed quantity as an input. It demonstrates the decision using newly written code. Finance retains authority to release the invoice.

[Back to my portfolio](../../README.md)
