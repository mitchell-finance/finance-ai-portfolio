"""Compare signed GBP balances. Positive differences mean more in the opening export."""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


def balances(filename, mapping=None):
    totals = defaultdict(Decimal)
    with Path(__file__).with_name(filename).open(newline="") as stream:
        for row in csv.DictReader(stream):
            project = row["project"]
            if mapping is not None:
                project = mapping[project]  # An unknown code stops the comparison.
            totals[row["account"], project] += Decimal(row["amount_gbp"])
    return totals


def by_account(rows):
    totals = defaultdict(Decimal)
    for (account, _), amount in rows.items():
        totals[account] += amount
    return totals


def differences(closing, opening):
    result = {}
    for key in sorted(closing.keys() | opening.keys()):
        delta = opening.get(key, 0) - closing.get(key, 0)
        if delta:
            result[key] = delta
    return result


def run():
    closing = balances("xero.csv")
    mapping = {"N01":"North", "S01":"South", "N07":"South", "HQ":"Central"}
    opening = balances("business-central.csv", mapping)
    print(f"Signed ledger total | closing {sum(closing.values()):,.2f} | opening {sum(opening.values()):,.2f} GBP")
    for account, amount in sorted(by_account(closing).items()):
        print(f"Account {account} | closing {amount:,.2f} | opening {by_account(opening)[account]:,.2f}")
    for (account, project), delta in differences(closing, opening).items():
        print(f"HOLD | {account} | {project} | opening less closing {delta:+,.2f} GBP")
    print("Finance checks the fictional project register: N07 belongs to North. Correct comparison mapping.")
    mapping["N07"] = "North"
    rerun = balances("business-central.csv", mapping)
    if differences(closing, rerun):
        raise ValueError("Project balances still differ")
    print("PASS | closing and opening agree by account and project.")
    print("Sign-off record | project reconciliation passed | cutover pending other checks.")
    print("Authorising role: client finance lead.")


if __name__ == "__main__":
    run()
