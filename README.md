# Stephen Mitchell

Practical AI implementation · Finance transformation · Systems migration  
**Mitchell Finance & Technology Ltd · Liverpool · Available for short projects across the UK**

I help teams collect the right debts, find unbilled work and check systems before switching. I build the integrations and work with your staff, retaining human review for decisions affecting money or a customer.

For a £30m construction business, I led the accounting migration from Xero to Business Central and reconciled costs by project before go-live.

I use sample records and figures throughout the walkthroughs so you can follow the decisions I describe.

## Three examples I would start with

- **Credit control.** A £500 receipt lands between preparing a £1,200 chaser and calling the customer. I block the old draft and put £700 back to finance for review. [See the call list and both drafts](demos/credit-control/README.md).
- **Xero to Business Central.** Every project total agrees, but split postings have moved cost between labour and materials. I trace the postings back to their source lines before signing off. [Follow the migration reconciliation](demos/migration/lineage.md).
- **Construction variations.** Site measured 110 metres and the certificate covers 100. I trace the £5,300 October valuation to its evidence and catch a £95 extraction against an £85 instruction. [Inspect the certificate, rate and prior billing](demos/variation-review/README.md).

## Working with a team

For a utilities contractor, I ran an in-person workshop with four office staff and managers using a completed job. A colleague went on to cost jobs independently and I checked their figures. [Discuss a project with me](https://mitchellfinance.co.uk/).

## Find a problem your team recognises

| If you need to… | Start here |
| --- | --- |
| Switch finance systems and trust the opening balances | [Migration sign-off](demos/migration/README.md) · [Trace split postings](demos/migration/lineage.md) |
| Clean supplier data before migration or integration | [Duplicate names, conflicting identifiers and bank changes](demos/data-cleaning/README.md) |
| Reconcile finance and operational records | [Unbilled jobs](demos/billing/README.md) · [Split payment allocations](demos/payment-run/allocations.md) |
| Automate routine work with human review | [Credit-control call list](demos/credit-control/README.md) · [AI extraction for month-end variations](demos/variation-review/README.md) |
| Connect purchasing, receiving and accounts payable | [Aperture: approval revisions and corrected receipts](demos/aperture/README.md) |
| Replace a period-end report with a decision about cash | [Can Friday’s supplier run be funded?](demos/cash-reporting/README.md) |
| Explain a change to an issued board pack | [Trace an £8,400 late invoice to a £2,400 profit movement](demos/month-end/README.md) |
| Forecast the cost of completing a job | [Programme delays, revised rates and accruals](demos/cost-to-complete/README.md) |
| Review a commercial proposal or update a sales forecast | [Partial quote amendments](demos/proposal-review/amendments.md) · [Partial orders and repeated CRM events](demos/crm-review/order-events.md) |
| Check a contract rate before billing | [Eight cases covering signed amendments, scope, dates and referral](demos/contract-review/README.md) |

## Run the examples

From the repository folder, use Python 3.10 or later. The checks run offline with the standard library.

```sh
python run_tests.py
python demos/credit-control/credit_review.py
python demos/contract-review/evaluate.py
```
