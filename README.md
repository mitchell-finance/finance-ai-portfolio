# Stephen Mitchell

Practical AI implementation · Finance transformation · Systems migration  
**Mitchell Finance & Technology Ltd · Liverpool · Available for short projects across the UK**

I help teams collect the right debts, find unbilled work and check systems before switching. I build the integrations and work with your staff, retaining human review for decisions affecting money or a customer.

For a £30m construction business, I led the accounting migration from Xero to Business Central and reconciled costs by project before go-live.

I use sample records and figures throughout the walkthroughs so you can follow the decisions I describe.

## Find a problem your team recognises

| If you need to… | Start here |
| --- | --- |
| Switch finance systems and trust the opening balances | [Migration sign-off](demos/migration/README.md) · [Trace split postings](demos/migration/lineage.md) |
| Clean supplier data before migration or integration | [Duplicate names, conflicting identifiers and bank changes](demos/data-cleaning/README.md) |
| Reconcile finance and operational records | [Unbilled jobs](demos/billing/README.md) · [Split payment allocations](demos/payment-run/allocations.md) |
| Automate routine work with human review | [Credit-control call list](demos/credit-control/README.md) · [AI extraction for month-end variations](demos/variation-review/README.md) |
| Connect purchasing, receiving and accounts payable | [Aperture: approval revisions and corrected receipts](demos/aperture/README.md) |
| Replace a period-end report with a decision about cash | [Can Friday’s supplier run be funded?](demos/cash-reporting/README.md) |
| Forecast the cost of completing a job | [Programme delays, revised rates and accruals](demos/cost-to-complete/README.md) |
| Review a commercial proposal or update a sales forecast | [Partial quote amendments](demos/proposal-review/amendments.md) · [Partial orders and repeated CRM events](demos/crm-review/order-events.md) |

## 1. Credit control before a customer call


**“I’m calling this customer in ten minutes. Which invoices should I raise?”**

For Example Works Ltd:

> **Raise DEMO-101: £1,200.00 overdue.**  
> Records checked: 26 November 2026, 09:00 GMT.
>
> **Refer DEMO-102 (£800.00) to an office colleague:** the customer queried the agreed quantity. Check the signed job record with the account manager.  
> Exclude paid, factored and not-yet-due invoices from the reminder.

After a £500.00 payment at 09:04, the 09:06 check **blocks the original draft** and reduces the request to **£700.00**. The replacement still needs finance review. This demo sends nothing.

[Worked example and draft →](demos/credit-control/README.md) · [Actual program output](demos/credit-control/expected-output.txt)

**Client work I delivered:** I built a Claude agent to read overdue Xero invoices, prepare a call list, separate factored accounts and draft Outlook chasers for finance review.

**What you can run here:** tested Python rules that check for changed balances. No AI model or live connectors.

**Possible extensions:** this customer view in Teams and Copilot Studio, proposed but not built or tested here.

## 2. Completed work that hasn’t reached the invoice

**“Which jobs have we finished but still haven’t billed, and what is holding each one up?”**

I connected Claude to construction software to identify unbilled work. At a utilities contractor, it helped find a misfiled shift report; the office corrected the reference and finance checked the draft.

**Worked result:** Hold the £750 draft for J103. Its signed report is filed against J104, which is already invoiced. Correct the reference and finance can review the existing draft. [Follow the job and the invoice](demos/billing/README.md).

## 3. Finance migration readiness: Xero to Business Central

**“The trial balance agrees. Are we actually ready to switch?”**

I led the migration on the client side, with 4PS as implementation partner. I checked the opening balances and the bank export before authorising finance cutover.

**Worked result:** Account 5100 agrees at £3,000, but North is £300 short and South £300 high. Hold sign-off until the project mapping is corrected and the check rerun. [Inspect the reconciliation and sign-off](demos/migration/README.md).

[Try the harder migration check](demos/migration/lineage.md): each project total agrees, yet two split postings misstate labour and materials.

## 4. The payment count and value agree. Would you release the file?

**Hold the £42,600 run.** One £2,400 invoice is in the bank file twice and another supplier’s £2,400 invoice is missing. Both lists still contain 18 payments. [Inspect the two exceptions and rerun the check](demos/payment-run/README.md).

## 5. Which variation value can finance support at month end?

The site diary records 110 metres, but the October certificate covers only 100. I compare the quantities in the correspondence with the signed certificate and deduct prior billing. That leaves **£5,300** for finance review. November’s approval adds £850. [Trace the figures back to the original words](demos/variation-review/README.md).

## Three more decisions for commercial and operations teams

- **Can sales issue this £48,000 proposal?** The buyer requested four assemblies by week six. The draft promises twelve and includes £700 of extra freight. [Compare the wording before and after review](demos/proposal-review/README.md).
- **How much does a two-week delay add to final cost?** I replace the old plant allowance and check the accrual. The margin falls by £2,600, even though £5,500 of hire remains to be recognised. [Follow the forecast bridge](demos/cost-to-complete/README.md).
- **Does a promised PO mean we’ve won the work?** Board approval is still pending. I keep the deal open and give the account manager a specific follow-up task. [Review the proposed CRM update](demos/crm-review/README.md).

## How I work with your team

We start with a real task. For a utilities contractor, I ran an in-person workshop for four office staff and managers using a completed job. A colleague subsequently costed jobs independently and I checked their figures.

I’m based in Liverpool and can travel across the UK for discovery, workshops, testing and training.

**Have a process like these?** [Tell me what is slowing your team down](https://mitchellfinance.co.uk/).

## Run the credit-control example

Python 3.10+; no packages or credentials. From the repository folder:

```sh
python demos/credit-control/credit_review.py
python -m unittest discover -s demos/credit-control -p "test_*.py" -v
```

The walkthrough explains the checks and their limits.
