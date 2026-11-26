# These supplier names look alike. Which records can I carry into the new system?

I built this example with sample supplier records and invented bank-account labels. My starting point is an awkward migration decision: a spelling difference can hide a duplicate, but a shared name can also hide two different businesses.

| Old ID | What I find | My decision |
| --- | --- | --- |
| L1 | Extra spaces and capitals. Entity and account agree with M1. | Propose M1 for owner review. |
| L2 | Name points to M1, while entity and account point to M2. | Hold. Check the original supplier record. |
| L3 | Name and entity agree, but the bank label has changed. | Hold for independent verification. |
| L4 | No corroborating identifiers. | Obtain evidence before creating or merging a record. |

I keep the original IDs and names intact. A normalised name is a search aid. It cannot authorise a supplier merge or a change to payment details. AI could suggest additional possible matches from abbreviations and descriptions; a data owner would still resolve conflicting evidence.

Run `python clean.py` and `python -m unittest -v`. The [matching rules and records](clean.py) deliberately use conservative exact identifiers and report one decision per input row. They produce a review list without updating the supplier master.

[Back to my portfolio](../../README.md)
