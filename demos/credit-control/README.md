# Credit control before a customer call

**“I’m calling this customer in ten minutes. Which invoices should I raise?”**

[← Back to Stephen Mitchell’s portfolio](../../README.md)

## The decision in one minute

For **Example Works Ltd**, raise **DEMO-101 for £1,200.00**. Refer the disputed £800.00 to an office colleague. Do not put the paid, factored or not-yet-due invoices in the reminder.

I’ve used five sample invoices for this call. The first balance check is dated **26 November 2026 at 09:00 GMT**.

| Invoice | Outstanding | What to do |
| --- | ---: | --- |
| DEMO-101 | £1,200.00 | Raise on the call; overdue since 14 November. |
| DEMO-102 | £800.00 | Refer to an office colleague: the agreed quantity is disputed. Check the signed job record with the account manager before chasing. |
| DEMO-103 | £0.00 | Already paid. No reminder. |
| DEMO-104 | £450.00 | Factored. Check with the invoice-finance provider before contacting the customer about payment. |
| DEMO-105 | £300.00 | Due 1 December. No overdue reminder. |

The **£2,750.00 total outstanding** is not the amount to chase. Only **£1,200.00** is currently eligible for the reminder.

## A payment changes the answer

The first draft asks about DEMO-101 only. It excludes the disputed amount and all the other invoices.

> Hello, could you confirm when we can expect payment of £1,200.00 for invoice DEMO-101? Thank you.

At **09:04**, a **£500.00** payment is allocated to DEMO-101. At **09:06**, finance checks again:

1. The original £1,200.00 draft fails the record check.
2. A new review reduces DEMO-101 to **£700.00**.
3. The replacement draft asks only for that remaining balance. It still needs finance to check the reference, balance and recipient and decide whether to send it.

> Hello, could you confirm when we can expect payment of £700.00 for invoice DEMO-101? Thank you.

This is the practical control: a draft based on an earlier balance cannot pass the demo’s current-record check after that balance changes. A separate test covers full payment, which removes the payment request entirely.

**[Read the actual output, including both drafts →](expected-output.txt)**

## Client work I delivered

I built a Claude credit-control agent that reads overdue invoices from Xero, prepares a call list, separates factored accounts and drafts chasers in Outlook for finance to review. I led a company-wide AI rollout for a construction business turning over about £30m.

The useful result is a clear next action with the exceptions visible. The person responsible for the customer or the money retains the decision.

## What you can run here

My call list groups the result by customer, explains each exclusion, prepares draft text and checks whether an earlier review still matches the latest supplied records.

It runs locally with **Python 3.10 or later** and the standard library. No installation of packages, credentials or network connection is needed. From the repository folder:

```sh
python demos/credit-control/credit_review.py
python -m unittest discover -s demos/credit-control -p "test_*.py" -v
```

On Windows, `py` can be used instead of `python` if that is how Python is installed. The demo always runs the fixed 26 November scenario so the expected output remains reproducible.

| File | What to inspect |
| --- | --- |
| [credit_review.py](credit_review.py) | Validation, customer decisions, draft text and the repeat check. |
| [data/first-review.json](data/first-review.json) | The five invoices at the first review. |
| [data/after-payment.json](data/after-payment.json) | The later snapshot with the £500.00 receipt recorded. |
| [test_credit_review.py](test_credit_review.py) | Tests for exceptions, customer isolation, changed payments and invalid or stale records. |
| [expected-output.txt](expected-output.txt) | Output captured from the executable example. |

### Checks and limits

Only a positive overdue balance on an open, undisputed, unfactored invoice can enter the draft. An invoice due today is not overdue. The demo uses the UTC date, which matches GMT for this November example. Invalid or unsupported input stops the review rather than producing a reminder. Other customers’ invoices cannot enter this customer’s draft.

The demo rejects future timestamps and snapshots more than ten minutes old relative to the supplied review time. Ten minutes is an illustrative setting, not a production service commitment. A timestamp in a file is not proof that a live ledger was refreshed.

The repeat check works against the latest snapshot supplied to it. It cannot discover a payment missing from that snapshot. There is no bank reconciliation, Xero connection, AI model, recipient lookup, Outlook draft creation or sending function here. Credit notes, unallocated receipts, multiple currencies and live factoring arrangements would need additional handling before real use.

## Possible extensions

A Teams and Copilot Studio version could give sales this view before a customer call. That is a **proposed implementation**, not something built or tested in this repository.

A live version would need authorised connectors, current payment and dispute data, appropriate customer access, and a recheck immediately before finance approves the message. The human review and responsibility for sending would remain explicit.
