"""Offline comparison of a fictional approved GBP run and bank export."""
import argparse
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["supplier", "invoice", "pence"]:
            raise ValueError("Expected supplier,invoice,pence")
        rows = []
        for line, row in enumerate(reader, start=2):
            supplier, invoice, amount = (row.get(k) for k in reader.fieldnames)
            if (None in row or not supplier or not invoice or not amount
                    or not amount.isascii() or not amount.isdigit() or int(amount) <= 0):
                raise ValueError(f"Invalid payment at line {line}")
            rows.append((supplier, invoice, int(amount)))
        if not rows:
            raise ValueError("Empty payment run")
        return rows


def gbp(pence):
    return f"GBP {pence // 100:,}.{pence % 100:02d}"


def compare(approved, exported):
    if len({(s, i) for s, i, _ in approved}) != len(approved):
        raise ValueError("Duplicate supplier/invoice in approved run; review the authority file")
    authority, bank = Counter(approved), Counter(exported)
    return authority - bank, bank - authority


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved", type=Path, default=HERE / "approved.csv")
    parser.add_argument("--export", type=Path, default=HERE / "bank-export.csv")
    args = parser.parse_args()
    try:
        approved, exported = read_rows(args.approved), read_rows(args.export)
        missing, excess = compare(approved, exported)
    except (ValueError, OSError, csv.Error) as error:
        print(f"HOLD | {error}")
        return 2
    for label, rows in (("Approved", approved), ("Bank file", exported)):
        print(f"{label}: {len(rows)} payments | {gbp(sum(p for _, _, p in rows))}")
    for label, differences in (("Missing", missing), ("Excess", excess)):
        for (supplier, invoice, pence), count in sorted(differences.items()):
            print(f"{label}: {count} x {supplier} / {invoice} / {gbp(pence)}")
    if missing or excess:
        print("HOLD | Regenerate the file and compare again before release.")
        return 1
    print("MATCH | Line comparison passed. Finance retains payment authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
