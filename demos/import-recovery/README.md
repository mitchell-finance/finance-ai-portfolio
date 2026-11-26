# Yesterday’s import finished. Where is the £825 invoice?

I built this offline support exercise with fictional invoices. The staging ledger contains S101 and S103. Looking only at the latest invoice would suggest the import had caught up. Before releasing the batch to finance, I compare every source invoice with the records that arrived.

| Daily control | Operations export | Finance staging before recovery | After recovery |
| --- | ---: | ---: | ---: |
| Invoice count | 3 | 2 | 3 |
| Net GBP | £3,625 | £2,800 | £3,625 |
| S102 for South | £825 | Missing | £825 |

**Detect.** I check the source export against the closed batch’s count and net value. I then compare invoice reference, customer and amount within the batch. This identifies S102 even though S103 arrived.

**Recover.** I stage the missing invoice in one database transaction. An unexpected reference or conflicting customer or value puts the batch on hold for the integration owner. If an insert fails halfway, the transaction rolls back. If the worker loses its acknowledgement after committing, it can reopen the database and repeat the comparison. The second attempt adds zero rows.

**Hand over.** I release the batch for finance review only after every source row matches and the target contains no extra rows. A discrepancy in posted accounts would need a separate correction approved by finance.

Run `python recover.py` and `python -m unittest -v` in this folder. The demonstration uses a temporary SQLite file, one closed batch, a trusted source manifest and whole pence. I model the daily control locally. A deployed service would also need a schedule, a named alert recipient and access to the source export and staging system.

[Source and recovery procedure](recover.py) · [Regression checks](test_recover.py) · [Back to my portfolio](../../README.md)
