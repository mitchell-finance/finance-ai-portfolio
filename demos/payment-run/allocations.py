"""Reconcile a fictional many-to-many payment schedule, using exact integer pence."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE approvals (
    invoice TEXT PRIMARY KEY NOT NULL, supplier TEXT NOT NULL, pence INTEGER NOT NULL
);
CREATE TABLE transfers (
    transfer TEXT PRIMARY KEY NOT NULL, beneficiary TEXT NOT NULL, pence INTEGER NOT NULL
);
CREATE TABLE allocations (
    transfer TEXT NOT NULL REFERENCES transfers, invoice TEXT NOT NULL REFERENCES approvals,
    pence INTEGER NOT NULL, PRIMARY KEY (transfer, invoice)
);
"""

# A LEFT JOIN also exposes an approved invoice or transfer with no allocation at all.
CHECKS = {
    "Invoice allocation difference": """
        SELECT a.invoice, COALESCE(SUM(x.pence), 0) - a.pence
        FROM approvals a LEFT JOIN allocations x USING (invoice)
        GROUP BY a.invoice, a.pence HAVING COALESCE(SUM(x.pence), 0) <> a.pence
        ORDER BY a.invoice""",
    "Transfer allocation difference": """
        SELECT t.transfer, COALESCE(SUM(x.pence), 0) - t.pence
        FROM transfers t LEFT JOIN allocations x USING (transfer)
        GROUP BY t.transfer, t.pence HAVING COALESCE(SUM(x.pence), 0) <> t.pence
        ORDER BY t.transfer""",
    "Wrong beneficiary": """
        SELECT x.transfer, x.invoice, a.supplier, t.beneficiary, x.pence
        FROM allocations x JOIN approvals a USING (invoice) JOIN transfers t USING (transfer)
        WHERE a.supplier <> t.beneficiary ORDER BY x.transfer, x.invoice""",
}


def reconcile(case):
    """Return all differences. Reject ambiguous records before calculating totals."""
    tables = ("approvals", "transfers", "allocations")
    if not isinstance(case, dict) or set(case) != set(tables):
        raise ValueError("Supply approvals, transfers and allocations")
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript(SCHEMA)
        for table in tables:
            rows = case[table]
            if not isinstance(rows, list) or (table != "allocations" and not rows):
                raise ValueError(f"Invalid or empty {table}")
            for row in rows:
                if (not isinstance(row, list) or len(row) != 3
                        or any(not isinstance(s, str) or not s.strip() for s in row[:2])
                        or type(row[2]) is not int or row[2] <= 0):
                    raise ValueError(f"Invalid {table} row; expected two identifiers and positive integer pence")
            try:
                db.executemany(f"INSERT INTO {table} VALUES (?, ?, ?)", rows)
            except sqlite3.IntegrityError as error:
                raise ValueError(f"Duplicate or unresolved reference in {table}") from error
        return {label: db.execute(query).fetchall() for label, query in CHECKS.items()}


def load_case():
    return json.loads(Path(__file__).with_name("allocation-case.json").read_text())


if __name__ == "__main__":
    case = load_case()
    report = reconcile(case)
    for label, rows in report.items():
        print(f"{label}: {len(rows)}")
        for row in rows:
            print("  " + " | ".join(map(str, row)))
    if any(report.values()):
        print("HOLD: finance must resolve exceptions. Amounts above are pence.")
        raise SystemExit(1)
    print("MATCH: ready for finance review.")
