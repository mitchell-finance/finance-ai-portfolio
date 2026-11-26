# Which completed jobs are still waiting to be billed?

**J103 is worth £750. The draft invoice already exists, but its supporting shift report is sitting on J104, a job that has already been invoiced.** Looking only for a draft would release it too soon. Looking only for a missing report could send someone back to site to recreate evidence the office already has.

| Job | First check | Office or finance decision |
| --- | --- | --- |
| J101 | £620 draft D21 matches signed report S11 | Finance can check and release the existing draft. |
| J102 | No shift report for £480 of completed work | Ask the supervisor for the report. |
| J103 | Draft D23 exists. S13 carries original reference J103 but was filed on J104 | Hold D23. Check the original job reference on the signed report. |
| J104 | £900 already invoiced | Skip billing even though a second report was filed here. |

I trace S13 back to the original job reference. Once the office confirms it, the filing reference can be corrected. On rerun, J103 has one supporting report and one matching £750 draft. Finance can now review D23. J102 stays on hold and J104 stays billed.

**Client work I delivered.** I connected Claude to construction software to identify completed work awaiting billing. For a utilities contractor, Claude helped identify a shift report filed against the wrong job. The office corrected the reference and finance checked the draft.

**What you can run here.** From this folder run `python billing.py`, then `python -m unittest -v`. The [fictional records](jobs.json) represent one fixed-price job per invoice with one required shift report. The correction is replayed in memory. Finance retains release authority. [Read the actual output](expected-output.txt).

**What if the office retries after a timeout?** Run `python retry_example.py`. A separate in-memory example saves a draft, then simulates a lost acknowledgement. On retry the same company and batch reference returns the existing draft. One draft awaits review. [Inspect the retry example](retry_example.py).

**Possible extensions.** A job billed in stages needs a check by valuation and invoice line. Two reports on one job are held for review in this example.

[Back to the portfolio](../../README.md)
