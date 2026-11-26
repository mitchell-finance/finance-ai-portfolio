# These supplier names look alike. Which records can I carry into the new system?

I built this example with sample supplier records and invented bank-account labels. My starting point is an awkward migration decision: a spelling difference can hide a duplicate, but a shared name can also hide two different businesses.

| Old ID | What I find | My decision |
| --- | --- | --- |
| L1 | Extra spaces and capitals. Entity and account agree with M1. | Propose M1 for owner review. |
| L2 | Name points to M1, while entity and account point to M2. | Hold. Check the original supplier record. |
| L3 | Name and entity agree, but the bank label has changed. | Hold for independent verification. |
| L4 | No corroborating identifiers. | Obtain evidence before creating or merging a record. |

I keep the original IDs and names intact. A normalised name is a search aid. It cannot authorise a supplier merge or a change to payment details. AI could suggest additional possible matches from abbreviations and descriptions; a data owner would still resolve conflicting evidence.

Run `python clean.py` and `python -m unittest -v`. The [matching rules and records](clean.py) deliberately use conservative exact identifiers and report one decision per input row. In the sample decision log the owner approved L1 against M1. The export contains that one mapping. L2 stays with the supplier data owner to resolve the legal entity, L3 goes to accounts payable for independent bank verification, and L4 needs supporting records from purchasing. The control accounts for all four source rows: one accepted, three pending. A later change to the reviewed bank label invalidates the approval on replay.

[Back to my portfolio](../../README.md)
