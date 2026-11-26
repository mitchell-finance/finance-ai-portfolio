"""Bridge the previous whole-job forecast to the revised forecast, in whole GBP."""
import json
from pathlib import Path


def bridge(case):
    old, revised = case["previous_allowance"], case["revised_quote"]
    for period in (old, revised):
        if any(type(period[k]) is not int or period[k] < 0 for k in ("weeks", "weekly_rate")):
            raise ValueError("Check hire period and rate")
    rows = case["ledger"]
    if len({row["ref"] for row in rows}) != len(rows):
        raise ValueError("Review duplicate ledger references")
    if any(type(row["amount"]) is not int or row["amount"] < 0 for row in rows):
        raise ValueError("Review ledger amount")
    allowance = old["weeks"] * old["weekly_rate"]
    hire = revised["weeks"] * revised["weekly_rate"]
    accrued = sum(row["amount"] for row in rows)
    if accrued > hire or allowance > case["previous_forecast"]:
        raise ValueError("Reconcile hire and previous allowance before forecasting")
    forecast = case["previous_forecast"] - allowance + hire
    return hire, hire - accrued, forecast, case["contract"] - forecast


if __name__ == "__main__":
    case = json.loads(Path(__file__).with_name("forecast.json").read_text())
    for label, value in zip(("Revised hire", "Hire still to recognise", "Forecast final cost",
                             "Forecast margin"), bridge(case)):
        print(f"{label}: GBP {value:,}")
