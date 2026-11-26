"""Read fictional construction and invoice records. All sample amounts are whole GBP."""
import json
from copy import deepcopy
from pathlib import Path


def assess(job, reports, invoices):
    ref, state, value = job
    bills = [b for b in invoices if b[1] == ref]
    if len(bills) > 1:
        return "Hold | check duplicate records or split billing with finance"
    if bills and bills[0][2] == "AUTHORISED":
        amount = bills[0][3]
        if type(amount) is not int or amount < 0:
            return "Hold | check authorised invoice amount"
        if amount != value:
            return f"Hold | finance to reconcile job less authorised invoice: GBP {value - amount:+,}"
        return "Already invoiced | skip billing"
    if state != "complete":
        return "Hold | job incomplete"
    evidence = [r for r in reports if ref in (r["original"], r["filed"])]
    if not evidence:
        return "Hold | shift report missing"
    if any(r["original"] != r["filed"] for r in evidence):
        return "Hold | conflicting job references on " + ", ".join(
            r["id"] for r in evidence if r["original"] != r["filed"])
    if len(evidence) != 1:
        return "Hold | check duplicate records"
    if not bills:
        return "Ready to prepare a draft | supporting report " + evidence[0]["id"]
    number, _, status, amount = bills[0]
    if status != "DRAFT" or amount != value:
        return "Hold | check invoice status and value"
    return f"Ready for finance review | {number}, GBP {value:,}, supported by {evidence[0]['id']}"


def run():
    data = json.loads(Path(__file__).with_name("jobs.json").read_text())
    for job in data["jobs"]:
        print(job[0], assess(job, data["reports"], data["invoices"]), sep=" | ")
    corrected = deepcopy(data["reports"])
    report = next(r for r in corrected if r["id"] == "S13")
    print(f"Office checks signed report S13: original {report['original']}; filed under {report['filed']}.")
    report["filed"] = report["original"]
    print("After correction:")
    for job in data["jobs"]:
        print(job[0], assess(job, corrected, data["invoices"]), sep=" | ")


if __name__ == "__main__":
    run()
