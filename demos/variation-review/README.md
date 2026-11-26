# The site says 110 metres are finished. How much can I put forward this month?

A fictional customer orders extra ducting on job V17. Six records and a site email tell different parts of the story. The original allowance was 100 metres at £80. A revised instruction replaces it with **120 metres in total at £85**. The site diary records 110 metres installed. On 31 October, the commercial manager has certified 100.

| At 31 October | Net value |
| --- | ---: |
| Revised instruction ceiling, 120 m × £85 | £10,200 |
| Measured work, 110 m × £85 | £9,350 |
| Certified value, 100 m × £85 | £8,500 |
| Less the amount already billed | £3,200 |
| **Amount to put to finance for review** | **£5,300** |

The £3,200 is an amount already invoiced. Deducting the first 40 metres at today's £85 rate would deduct £200 too much. A second trap is the site email saying all 110 metres “look fine”. The signed certificate explicitly leaves ten metres awaiting inspection.

**What changes on 3 November?** A new signed certificate clears the ten metres. With prior billing still at £3,200 in the sample, the amount available for review becomes £6,150. That is an £850 increase. If October’s £5,300 had since been invoiced, finance would first update the billing register and only £850 would remain.

## Where AI earns its place

Read the [seven fictional source records](evidence.json), then inspect the [saved AI interpretation](interpretation.json). An AI assistant authored the scenario and extracted the quantities and amounts into a candidate table, keeping the supporting words with each claim. The reviewer’s task is to decide whether each quotation actually supports the extracted value, unit and meaning. For instance, “120 metres” is a replacement ceiling, while “110 metres” in the diary is cumulative work completed. Neither grants authority to invoice.

The Python replay checks citations, source types, missing records and the cut-off before applying the agreed arithmetic. A quotation can be authentic while a number extracted from it is wrong. The reviewer must check those numbers against the originals before relying on the result. The fixtures are illustrative and do not measure model accuracy on unseen documents.

**Client work I delivered.** In my Finance Director role I worked with the quantity surveyor and directors to reconcile project costs and explain differences in the management accounts. This variation review is a newly built portfolio demonstration.

**What you can run here.** From this folder, run `python review.py` and `python -m unittest -v` (Python 3.10+). The replay uses the saved extraction offline. Try changing the prior-billing record and its matching extraction to £8,500 and rerunning the November check. This example assumes one job, a retrospectively applicable revised rate, cumulative snapshots and one authorised source per record type. Finance owns release. Revenue recognition, VAT, retention and contractual entitlement require separate assessment.

**Possible extensions.** For a pilot, give a model a previously unseen variation pack and compare its extracted values and evidence against a quantity surveyor’s independent review. Measure missed revisions, unsupported approvals and the value of differences before considering integration.

[Back to the portfolio](../../README.md)
