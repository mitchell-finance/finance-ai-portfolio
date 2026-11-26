# Would you release this payment run?

**18 approved payments. 18 bank-file lines. £42,600 on both sides. Hold the file.**

| Supplier and invoice | Approved | Bank file | Decision |
| --- | ---: | ---: | --- |
| SUP-01 / INV-101 | £2,400 once | £2,400 twice | Remove the extra instruction when regenerating the file. |
| SUP-02 / INV-102 | £2,400 once | Missing | Restore the omitted instruction. |

Both errors are for the same amount. Counting rows or adding up the pounds gives finance false reassurance. I compare each supplier, invoice and amount, including the number of times that combination appears. The order of the file can change.

**Client work I delivered.** During a finance migration I checked a bank export against the approved payment count and value. This fictional example explores a further check for offsetting errors.

**What you can run here.** In this directory, run `python check.py` to compare the [approved run](approved.csv) and [fictional export](bank-export.csv). The program prints both differences and exits with status 1 for a hold. To try the correction yourself, copy the export, replace the second SUP-01 / INV-101 with SUP-02 / INV-102, retain the amount, and run `python check.py --export corrected.csv`. A match exits with status 0. Invalid input exits with status 2. Run `python -m unittest -v` for the checks. [See both runs](expected-output.txt).

The sample assumes one GBP payment per approved supplier invoice and an export that retains both references. It uses fictional supplier IDs. A match confirms the listed references and amounts. Finance still checks beneficiary details and authorises the actual payment.

**Try the more complex case.** Three transfers settle three invoices, but one invoice is split and another transfer combines invoices. Every invoice and bank transfer adds up, yet two remittance lines identify the wrong supplier. [Trace the £5,000 allocation schedule](allocations.md).

**Possible extensions.** Compare beneficiary identifiers against a separately approved supplier master before release.

[Back to the portfolio](../../README.md)
