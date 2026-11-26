# The trial balance agrees. Are we ready to switch?

**Hold the cutover decision.** Both exports show £3,000 of costs in account 5100. One opening project code, N07, has been mapped to South. The project register says it belongs to North. Both teams could sign off their ledger accounts and still start the month with the wrong job margins.

| Project in account 5100 | Closing Xero | Opening comparison | Difference |
| --- | ---: | ---: | ---: |
| North | £1,800 | £1,500 | −£300 |
| South | £1,200 | £1,500 | +£300 |

The finance reviewer checks the project register and corrects N07 in the comparison mapping. The rerun gives North £1,800 and South £1,200. This sample fixes an interpretation of the opening export. An error in the posted ledger would need a correction there and a fresh export.

**Illustrative sign-off record.** The closing and opening balances agree by account and project after correction. The client finance lead would authorise cutover once the other agreed tests pass. This single check clears the project reconciliation only.

**Client work I delivered.** In a separate independent assignment alongside my Finance Director role, I led the client-side Xero-to-Business Central finance migration with 4PS as implementation partner. I reconciled by account and project, tested the bank export against the approved payment count and value, and authorised finance cutover. Finance went live in the planned quarter, with around 50 system users across the business.

**What you can run here.** Run `python migration.py` and `python -m unittest -v` from this folder. Inspect the fictional [closing export](xero.csv), [opening export](business-central.csv) and [actual output](expected-output.txt). Amounts are signed GBP for one cutover date. The example reads both exports locally.

**Possible extensions.** A separate bank-export check could compare the payment count and value to the approved run before anyone releases the file.

[Back to the portfolio](../../README.md)
