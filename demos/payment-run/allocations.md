# When every invoice and transfer adds up, who actually gets paid?

I use sample invoices, transfers and remittance records to show how I’d check a payment split across two transfers.

**Hold the £5,000 file.** North is due £4,000 across two invoices and South is due £1,000. North's second invoice is split between transfers. The bank file has the right amounts for both beneficiaries, and each invoice is fully allocated. The remittance schedule nevertheless tells each supplier that £1,000 settles the other supplier's invoice.

| Transfer | Bank beneficiary | Allocation record | Finding |
| --- | --- | --- | --- |
| T01 · £3,000 | North | £2,800 against A17 and £200 against A18 | Both belong to North. |
| T02 · £1,000 | North | £1,000 against B09 | B09 belongs to South. |
| T03 · £1,000 | South | £1,000 against A18 | A18 belongs to North. |

I would send the **allocation schedule** back for correction. In this case the cash totals by beneficiary already agree. Changing the bank amounts would introduce a new error. Allocate T02 to A18 and T03 to B09, then rerun all three checks.

**Run the evidence.** From this directory run `python allocations.py` (status 1 means hold), then `python -m unittest -v test_allocations`. The [data file](allocation-case.json) contains the approved invoices, transfers and allocation rows in pence. The [Python and SQL](allocations.py) reconcile each invoice, each transfer and each relationship. The tests exercise the corrected schedule, missing allocations, duplicate rows and unknown references.

This independent example assumes unique invoice IDs and trusted supplier identifiers on approved invoices and bank transfers. Verifying actual beneficiary account details is a separate control.

[Back to the payment-run example](README.md)
