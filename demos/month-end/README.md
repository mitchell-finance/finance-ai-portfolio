# Why did October profit change after I issued the board pack?

I use sample figures to show how I’d explain a late supplier invoice. The board saw October profit of **£42,000**. On 5 November, finance receives an **£8,400** invoice for work completed on 29 October. Before proposing a change I check the job *and the work reference*: £6,000 for that work was already accrued.

| October profit bridge | Amount |
| --- | ---: |
| Issued pack | £42,000 |
| Release the estimate for J17 / W8 | +£6,000 |
| Recognise INV-47 for the same work | −£8,400 |
| **Proposed profit if October is reopened** | **£39,600** |

**My board note:** “The final supplier charge for job J17 was £2,400 above our October estimate. If we reopen October, reported profit falls by that amount to £39,600.” The original issued pack remains available. The finance director decides how to treat the late invoice under the business’s close policy.

### Handover for the finance colleague preparing the pack

1. On Windows with Python 3.10 or later installed, double-click **Review October.cmd** in the downloaded example. Select **1** to use the 24 October export. Its £132,000 total looks right, but it ends a week early. The report holds.
2. Obtain the export through **31 October**. Run the launcher again and select **2** to use that file. In live work, confirm the reporting period and completeness at source.
3. Compare the [issued figures](issued.json) and [invoice](invoice.json). Confirm that J17 / W8 represents the same work, then check the £2,400 movement. Keep the issued pack and send the proposed bridge to the finance director for a decision.

**Technical route.** Run `python pack.py` for the corrected input or `python pack.py --export stale-project-costs.json` to reproduce the hold. Run `python -m unittest -v` from this folder. The comparison reads local files, uses whole GBP and assumes one invoice fully replaces one accrual. A changed unrelated cost or mismatched work reference requires separate investigation. It prepares a management-report comparison without posting journals.

[Back to my portfolio](../../README.md)
