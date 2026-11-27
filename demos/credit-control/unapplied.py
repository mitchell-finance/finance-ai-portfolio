"""Replay a single identified customer receipt against a pre-allocation snapshot."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from credit_review import DataError, load_snapshot, money, review_customer

HERE = Path(__file__).parent


def position(snapshot, receipt, advice, now):
    customer = receipt["customer_id"]
    amount = receipt["pence"]
    if type(amount) is not int or amount <= 0 or not receipt["reference"]:
        raise DataError("Check bank receipt amount and reference")
    ledger = deepcopy(snapshot)
    review = review_customer(ledger, customer, now)
    open_total = sum(row.outstanding_pence for row in review.decisions)
    if amount > open_total:
        raise DataError("Customer credit balance needs separate review")
    if not advice:
        return open_total, amount, open_total - amount, None

    targets = set()
    for item in advice:
        if (item["receipt"], item["customer_id"]) != (receipt["reference"], customer):
            raise DataError("Remittance does not identify this customer receipt")
        targets.add(item["invoice"])
    if len(targets) != 1:
        raise DataError("Conflicting remittances for the same receipt")
    target = targets.pop()
    invoice = next((row for row in ledger["invoices"]
                    if row["reference"] == target and row["customer_id"] == customer), None)
    if invoice is None or amount != invoice["gross_pence"] - invoice["received_pence"]:
        raise DataError("Hold for review: expected one matching invoice balance")
    invoice["received_pence"] += amount
    review = review_customer(ledger, customer, now)
    remaining = sum(row.outstanding_pence for row in review.decisions)
    return remaining, 0, remaining, review.draft


def main():
    case = load_snapshot(HERE / "data" / "unapplied-receipt.json")
    now = datetime.fromisoformat(case["snapshot"]["checked_at"])
    for label, advice in (("Bank receipt only", []), ("Remittance received", [case["advice"]]),
                          ("Duplicate remittance", [case["advice"]] * 2)):
        outstanding, unapplied, net, draft = position(case["snapshot"], case["receipt"], advice, now)
        print(f"{label} | invoices {money(outstanding)} | unapplied {money(unapplied)} | net {money(net)}")
        print(draft or "Hold invoice-specific chaser. Ask for remittance advice.")


if __name__ == "__main__":
    main()
