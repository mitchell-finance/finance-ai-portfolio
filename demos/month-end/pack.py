"""Prepare an October comparison. Source files are read-only. Amounts are whole GBP."""
import argparse
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def compare(issued, invoice, export):
    end = date.fromisoformat(issued["period_end"])
    if date.fromisoformat(export["through"]) != end:
        raise ValueError(f"Project costs cover {export['through']}; need {end}. Replace the export.")
    if export["other_costs_gbp"] != issued["other_costs_gbp"]:
        raise ValueError("Other project costs changed. Reconcile that movement separately.")
    accrual = issued["accrual"]
    if (invoice["job"], invoice["work_ref"]) != (accrual["job"], accrual["work_ref"]):
        raise ValueError("Invoice and accrual cover different work. Ask the job owner.")
    if not date.fromisoformat(invoice["work_completed"]) <= end < date.fromisoformat(invoice["received"]):
        raise ValueError("Review the work date and receipt date before using the late-invoice bridge.")
    amounts = [issued["revenue_gbp"], export["other_costs_gbp"], accrual["gbp"], invoice["net_gbp"]]
    if any(type(v) is not int or v < 0 for v in amounts):
        raise ValueError("Expected non-negative whole GBP amounts.")
    revenue, other, estimate, actual = amounts
    return revenue - other - estimate, estimate, actual, revenue - other - actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, default=HERE / "project-costs.json")
    args = parser.parse_args()
    try:
        previous, released, invoice, revised = compare(
            read(HERE / "issued.json"), read(HERE / "invoice.json"), read(args.export))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print("HOLD |", exc)
        return 1
    print(f"Issued October profit: GBP {previous:,}")
    print(f"Release matched accrual: +GBP {released:,}")
    print(f"Recognise supplier invoice: -GBP {invoice:,}")
    print(f"Proposed October profit: GBP {revised:,} | movement: GBP {revised - previous:+,}")
    print("Decision pending: finance director reviews whether to reopen October.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
