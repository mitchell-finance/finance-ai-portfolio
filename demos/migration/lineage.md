# Both project margins agree. Can I trust the labour and materials figures?

I built this example with sample closing and opening entries to show why I check costs by **account within each project** before signing off. The company trial balance agrees. North and South each have the right total cost. Even the company-wide labour and materials totals agree. Yet two errors would send a project manager looking for the wrong cause of an overspend.

| Opening less closing | Labour | Materials | Total cost difference |
| --- | ---: | ---: | ---: |
| North | −£300.25 | +£300.25 | £0.00 |
| South | +£300.25 | −£300.25 | £0.00 |
| Both projects | £0.00 | £0.00 | £0.00 |

**My decision is to hold the cost breakdown.** The four differences come from two opening lines. B02 carries part of the labour on closing line X01 to South. B06 carries the same amount of materials from X04 to North. Each source line was split during conversion, so comparing the number of rows would also be misleading.

I trace each opening line to its source, check the signed pence reconstruct that source balance and compare its account and project. The demonstration replays two reviewed project corrections on a copy and repeats all the checks. A separate test swaps two source references while preserving every financial total. Only the source-line check catches it.

**Run it.** From this directory run `python lineage.py` and `python -m unittest -v test_lineage`. Compare the [closing entries](closing-lines.csv), [opening entries](opening-lines.csv) and [actual output](lineage-output.txt). I use a common account and project vocabulary here. On a live migration I’d first validate the crosswalk and the provenance of the source IDs, and obtain independent evidence for any approved reclassification.

[Back to the migration walkthrough](README.md)
