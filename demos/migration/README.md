# The trial balance agrees. Are we ready to switch?

I reconciled balances by account and project before go-live. Here I’ve used sample figures to show how a £300 posting can land on the wrong project even when the trial balance agrees.

**Hold the cutover decision.** Both exports show £3,000 of costs in account 5100. One opening project code, N07, has been mapped to South. The project register says it belongs to North. Both teams could sign off their ledger accounts and still start the month with the wrong job margins.

| Project in account 5100 | Closing Xero | Opening comparison | Difference |
| --- | ---: | ---: | ---: |
| North | £1,800 | £1,500 | −£300 |
| South | £1,200 | £1,500 | +£300 |

I check the project register and correct N07 in the comparison mapping. The rerun gives North £1,800 and South £1,200. Here I correct how the opening export is mapped. An error in the posted ledger would need a correction there and a fresh export.

**Illustrative sign-off record.** The closing and opening balances agree by account and project after correction. The client finance lead would authorise cutover once the other agreed tests pass. This single check clears the project reconciliation only.

**Client work I delivered.** On an independent migration assignment, I led the client-side Xero-to-Business Central finance migration with 4PS as implementation partner. I reconciled by account and project, tested the bank export against the approved payment count and value, and authorised finance cutover. Finance went live in the planned quarter, with around 50 system users across the business.

**What you can run here.** Run `python migration.py` and `python -m unittest -v` from this folder. Inspect the [closing export](xero.csv), [opening export](business-central.csv) and [actual output](expected-output.txt). Amounts are signed GBP for one cutover date. The example reads both exports locally.

I also compare the proposed bank file with the approved payment run before release. [See the payment example where the count and value agree but two invoice references are wrong](../payment-run/README.md).

For this cutover I expect three closing rows and four opening rows from the sample export controls. An empty or short file stops the comparison. Row counts alone cannot detect substituted transactions; the source-line walkthrough covers that separate check.

[Back to the portfolio](../../README.md)

**A harder cutover decision:** [Both project margins agree. Can I trust the labour and materials figures?](lineage.md) Follow two split postings through four offsetting differences and test their source references.
