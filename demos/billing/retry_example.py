"""Fictional workshop example. Run with Python 3.10+. Uses an in-memory database."""
import sqlite3


def prepare(db, company, batch, interrupt=False):
    # A unique business reference survives a lost acknowledgement from the worker.
    with db:
        inserted = db.execute(
            "INSERT INTO drafts VALUES (?, ?) ON CONFLICT(company, batch) DO NOTHING",
            (company, batch),
        ).rowcount
    if interrupt:
        raise TimeoutError("Worker stopped after saving the draft")
    return "Draft prepared" if inserted else "Existing draft found"


def run():
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE drafts (company TEXT NOT NULL, batch TEXT NOT NULL,"
                   " PRIMARY KEY (company, batch))")
        try:
            prepare(db, "Example Works", "BATCH-17", interrupt=True)
        except TimeoutError as error:
            print("First attempt:", error)
        print("Retry:", prepare(db, "Example Works", "BATCH-17"))
        print("Drafts awaiting finance review:", db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0])
        assert db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0] == 1
        assert prepare(db, "Second Example", "BATCH-17") == "Draft prepared"


if __name__ == "__main__":
    run()
