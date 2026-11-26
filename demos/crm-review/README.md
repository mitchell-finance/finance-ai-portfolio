# Did the buyer place the order?

I built this example with sample meeting notes to show how I’d review a proposed CRM update before it changes the sales forecast.

> **Buyer:** “We’ll raise the PO once the board approves it.”
>
> **Account manager:** “I’ll send the board pack on Friday.”

The candidate update marks the deal **Won**. I’d keep it at **Proposal sent**. The buyer has described what happens *after* approval. The order register contains no verified PO for this opportunity.

There is still a useful update to make. I’d propose a task for the account manager to send the board pack on Friday, with their own words beside it. The salesperson confirms the calendar date and task wording before saving. If a verified order later arrives for the right opportunity, the stage change goes back for review.

**What runs here.** From this folder run `python review.py` and `python -m unittest -v`. The [meeting pack](meeting.json) includes the conflicting candidate update, the quotations and an order register. The code checks the evidence references, action owner and order match. It leaves the existing stage intact.

**Where I’d use AI.** Suggest tasks and extract buying signals from meeting transcripts. This offline example starts with a prepared candidate. A speaker match alone cannot prove that a paraphrase is faithful, so the reviewer sees the exact quotation. A verified PO is the illustrative stage rule for this business.

[Read the actual program output](expected-output.txt)

[Back to my portfolio](../../README.md)

[Advanced case: reconcile partial orders, late revisions and repeated events](order-events.md).
