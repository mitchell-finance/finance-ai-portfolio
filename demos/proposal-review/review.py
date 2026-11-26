"""Compare reviewed terms from one quote pack. Amounts are whole GBP excluding VAT."""
import json
from pathlib import Path


def review(pack):
    request, estimate, draft = (pack[k] for k in ("customer", "costing", "draft"))
    issues = []
    if draft["price"] != estimate["price"] or draft["units"] != request["units"]:
        issues.append("Sales: reconcile the quantity and price to the approved pack.")
    if (draft["promised_first_batch"], draft["weeks"]) != (request["first_batch"], request["weeks"]):
        issues.append(f"Operations: {request['ref']} requests {request['first_batch']} units by week "
                      f"{request['weeks']}; {draft['ref']} promises {draft['promised_first_batch']} "
                      f"by week {draft['weeks']}. Confirm capacity and dates.")
    extra = max(0, draft["deliveries"] - estimate["deliveries"]) * estimate["extra_freight_each"]
    if draft["deliveries"] != estimate["deliveries"]:
        issues.append(f"Commercial director: {draft['deliveries']} deliveries offered; "
                      f"{estimate['deliveries']} costed in {estimate['ref']}. Review freight.")
    return issues, extra, draft["price"] - estimate["cost"] - extra


if __name__ == "__main__":
    pack = json.loads(Path(__file__).with_name("quote.json").read_text())
    issues, extra, profit = review(pack)
    print(pack["draft"]["text"])
    print(*issues, sep="\n")
    print(f"Extra freight if absorbed: GBP {extra:,}; revised gross profit: GBP {profit:,}.")
    print("HOLD for review" if issues else "Compared terms agree; sales reviews before issue.")
