# Stephen Mitchell

Practical AI implementation · Finance transformation · Systems migration  
**Mitchell Finance & Technology Ltd · Liverpool · Available for short projects across the UK**

I help teams collect the right debts, find unbilled work and check systems before switching. I build the integrations and work with your staff, retaining human review for decisions affecting money or a customer.

For a £30m construction business, I led the accounting migration from Xero to Business Central and reconciled costs by project before go-live.

## 1. Credit control before a customer call

**“I’m calling this customer in ten minutes. Which invoices should I raise?”**

For fictional customer Example Works Ltd:

> **Raise DEMO-101: £1,200.00 overdue.**  
> Records checked: 26 November 2026, 09:00 GMT — fictional snapshot.  
> **Refer DEMO-102 (£800.00) to an office colleague:** the customer queried the agreed quantity. Check the signed job record with the account manager.  
> Exclude paid, factored and not-yet-due invoices from the reminder.

After a £500.00 payment at 09:04, the 09:06 check **blocks the original draft** and reduces the request to **£700.00**. The replacement still needs finance review. This demo sends nothing.

[Worked example and draft →](demos/credit-control/README.md) · [Actual program output](demos/credit-control/expected-output.txt)

**Client work I delivered:** a Claude agent reading overdue Xero invoices, preparing a call list, separating factored accounts and drafting Outlook chasers for finance review.

**What you can run here:** tested Python rules with fictional records and checks for changed balances. No AI model or live connectors.

**Possible extensions:** this customer view in Teams and Copilot Studio, proposed but not built or tested here.

## 2. Completed work that hasn’t reached the invoice

**“Which jobs have we finished but still haven’t billed, and what is holding each one up?”**

I connected Claude to construction software to identify unbilled work. At a utilities contractor, it helped find a misfiled shift report; the office corrected the reference and finance checked the draft.

**Worked result:** Hold the £750 draft for J103. Its signed report is filed against J104, which is already invoiced. Correct the reference and finance can review the existing draft. [Follow the job and the invoice](demos/billing/README.md).

## 3. Finance migration readiness: Xero to Business Central

**“The trial balance agrees. Are we actually ready to switch?”**

In a separate independent assignment alongside my Finance Director role, I led the client-side migration with 4PS as implementation partner, reconciling by account and project before authorising finance cutover.

**Worked result:** Account 5100 agrees at £3,000, but North is £300 short and South £300 high. Hold sign-off until the project mapping is corrected and the check rerun. [Inspect the reconciliation and sign-off](demos/migration/README.md).

## 4. The payment count and value agree. Would you release the file?

**Hold the £42,600 run.** One £2,400 invoice is in the bank file twice and another supplier’s £2,400 invoice is missing. Both lists still contain 18 payments. [Inspect the two exceptions and rerun the check](demos/payment-run/README.md).

## 5. Which variation value can finance support at month end?

The site diary records 110 metres, but the October certificate covers only 100. A saved AI reading of the correspondence and a dated reconciliation show **£5,300** for finance review after prior billing. November’s approval adds £850. [Trace the figures back to the original words](demos/variation-review/README.md).

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
