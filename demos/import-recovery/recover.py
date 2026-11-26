"""Recover one closed batch of fictional GBP invoices into a local staging ledger."""
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


def initialise(db):
    db.execute("""CREATE TABLE IF NOT EXISTS staged (
        batch TEXT NOT NULL, invoice TEXT NOT NULL, customer TEXT NOT NULL,
        pence INTEGER NOT NULL, PRIMARY KEY(batch, invoice))""")


def closed_batch(rows, expected_count, expected_pence):
    source = {}
    for invoice, customer, pence in rows:
        if not invoice or not customer or type(pence) is not int or pence <= 0 or invoice in source:
            raise ValueError("Invalid or duplicate source invoice")
        source[invoice] = (customer, pence)
    if not source or len(source) != expected_count or sum(p for _, p in source.values()) != expected_pence:
        raise ValueError("Source export differs from the closed batch controls")
    return source


def inspect(db, batch, source):
    staged = {invoice: (customer, pence) for invoice, customer, pence in db.execute(
        "SELECT invoice, customer, pence FROM staged WHERE batch = ?", (batch,))}
    missing = sorted(source.keys() - staged.keys())
    unexpected = sorted(staged.keys() - source.keys())
    changed = sorted(key for key in source.keys() & staged.keys() if source[key] != staged[key])
    return missing, unexpected, changed


def recover(db, batch, source):
    # Hold the write lock from the comparison through the final check.
    with db:
        db.execute("BEGIN IMMEDIATE")
        missing, unexpected, changed = inspect(db, batch, source)
        if unexpected or changed:
            raise ValueError(f"Hold for owner: unexpected {unexpected}, conflicting {changed}")
        db.executemany("INSERT INTO staged VALUES (?, ?, ?, ?)",
                       [(batch, key, *source[key]) for key in missing])
        if any(inspect(db, batch, source)):
            raise ValueError("Reconciliation failed before commit")
    return missing


ROWS = [("S101", "North", 120000), ("S102", "South", 82500), ("S103", "West", 160000)]
BATCH = "November-24"


def main():
    source = closed_batch(ROWS, 3, 362500)
    with TemporaryDirectory() as folder:
        path = Path(folder) / "staging.db"
        with closing(sqlite3.connect(path)) as db:
            initialise(db)
            with db:
                db.executemany("INSERT INTO staged VALUES (?, ?, ?, ?)",
                               [(BATCH, *ROWS[0]), (BATCH, *ROWS[2])])
            missing, _, _ = inspect(db, BATCH, source)
            print(f"Daily control: source {len(source)} invoices; missing from staging:", ", ".join(missing))
            print("Recovered:", ", ".join(recover(db, BATCH, source)))
        # The worker restarts after commit without having acknowledged the recovery.
        with closing(sqlite3.connect(path)) as db:
            print("Replay after lost acknowledgement: rows inserted =", len(recover(db, BATCH, source)))
            count, total = db.execute("SELECT COUNT(*), SUM(pence) FROM staged WHERE batch=?",
                                      (BATCH,)).fetchone()
            print(f"Reconciled by invoice, customer and value: {count} invoices, {total} pence")


if __name__ == "__main__":
    main()
