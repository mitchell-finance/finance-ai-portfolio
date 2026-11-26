# The price agrees. What have we promised?

I built this example with a sample manufacturing enquiry. A buyer has requested 12 assemblies. Sales has quoted the £48,000 price in the approved costing. I’d still hold the proposal.

**Draft:** “We will deliver all twelve assemblies within six weeks. Three deliveries are included in the price.”

**Buyer’s words:** “We need the first four assemblies within six weeks. Please confirm the schedule for the other eight.”

**My suggested wording before internal approval:** “You’ve requested four assemblies within six weeks. We’ll confirm that date and the schedule for the remaining eight with operations. Our price allows for one delivery. We’ll confirm the cost of split deliveries before you place the order.”

| Decision | Evidence | Who decides |
| --- | --- | --- |
| Can we promise a date? | RFQ-12 requests four by week six. Q-17 promises twelve. Even the first four need a capacity check. | Operations |
| Who pays for two extra deliveries? | EST-04 includes one. At £350 each, the extra two reduce gross profit from £12,000 to £11,300 if absorbed. | Commercial director |

**What runs here.** From this folder run `python review.py` and `python -m unittest -v`. The [quote pack](quote.json) pairs the source wording with structured terms. The script compares those terms and calculates the freight exposure. The wording above is my suggested edit.

**Where I’d use AI.** Extract the proposed commitments from successive drafts and return the exact sentence beside each one. The offline comparison assumes those extracted terms have been checked. It cannot establish factory capacity or approve a concession.

[Read the actual program output](expected-output.txt)

[Back to my portfolio](../../README.md)

[Advanced case: carry terms forward across partial amendments](amendments.md).
