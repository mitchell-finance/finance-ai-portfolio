# The site says 110 metres are finished. How much can I put forward this month?

I built this example using sample correspondence for an order of extra ducting on job V17. I’d start by comparing the instruction, the site diary and the signed certificate. The original allowance was 100 metres at £80. A revised instruction replaces it with **120 metres in total at £85**. The site diary records 110 metres installed. On 31 October, the commercial manager has certified 100.

| At 31 October | Net value |
| --- | ---: |
| Revised instruction ceiling, 120 m × £85 | £10,200 |
| Measured work, 110 m × £85 | £9,350 |
| Certified value, 100 m × £85 | £8,500 |
| Less the amount already billed | £3,200 |
| **Amount to put to finance for review** | **£5,300** |

The £3,200 is an amount already invoiced. Deducting the first 40 metres at today's £85 rate would deduct £200 too much. A second trap is the site email saying all 110 metres “look fine”. The signed certificate explicitly leaves ten metres awaiting inspection.

**What changes on 3 November?** A new signed certificate clears the ten metres. With prior billing still at £3,200, the amount available for review becomes £6,150. That is an £850 increase. If October’s £5,300 had since been invoiced, finance would first update the billing register and only £850 would remain.

## Where AI earns its place

I use AI to pick out quantities and amounts from the [seven source records](evidence.json). I keep the [extracted figures beside the words they came from](interpretation.json) so I can check what each figure means. For instance, “120 metres” is a replacement ceiling, while “110 metres” in the diary is cumulative work completed. Neither grants authority to invoice.

The Python replay checks citations, source types, missing records and the cut-off before applying the agreed arithmetic. A quotation can be authentic while a number extracted from it is wrong. If I change the saved I2 rate from £85 to £95 while keeping its genuine quotation, October would be overstated by £1,000. Run the wrong-rate test to see the replay stop at I2 before producing a value. The check recognises the single whole-pound “£85 per metre” wording in these instructions. Other terms and units need a reviewer. I would test extraction accuracy on unseen documents before using this on a live job.

**Client work I delivered.** I worked with the quantity surveyor and directors to reconcile project costs and explain differences in the management accounts.

**What you can run here.** From this folder, run `python review.py` and `python -m unittest -v` (Python 3.10+). The replay uses the saved extraction offline. Try changing the prior-billing record, its saved quotation and its extracted amount to £8,500 and rerunning the November check. This example assumes one job, a retrospectively applicable revised rate, cumulative snapshots and one authorised source per record type. Finance owns release. Revenue recognition, VAT, retention and contractual entitlement require separate assessment.

**Possible extensions.** For a pilot, give a model a previously unseen variation pack and compare its extracted values and evidence against a quantity surveyor’s independent review. Measure missed revisions, unsupported approvals and the value of differences before considering integration.

I also check the extracted certified quantity against the signed V17 certificate wording used in this pack. Changing October from 100 to 110 metres leaves the quotation intact but blocks the £850 overstatement. Unrecognised certificate wording requires manual review.

[Back to the portfolio](../../README.md)
