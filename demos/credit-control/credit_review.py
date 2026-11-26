"""Fictional customer review: standard library only; no model, connector or sending."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import sys


class DataError(ValueError):
    """Input records cannot safely support a review."""


class ReviewBlocked(ValueError):
    """A draft must not proceed on the evidence supplied."""


@dataclass(frozen=True)
class Decision:
    reference: str
    outstanding_pence: int
    action: str
    explanation: str


@dataclass(frozen=True)
class Review:
    customer_id: str
    customer_name: str
    checked_at: datetime
    freshness_limit: timedelta
    decisions: tuple[Decision, ...]
    amount_to_raise_pence: int
    draft: str | None
    _signature: tuple = field(repr=False)


def money(pence):
    return f"£{pence // 100:,}.{pence % 100:02d}"


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise DataError(f"{label} must be non-empty text.")
    return value


def _timestamp(value, label):
    try:
        result = datetime.fromisoformat(_text(value, label))
    except ValueError as exc:
        raise DataError(f"{label} must be an ISO timestamp with a timezone.") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise DataError(f"{label} needs a timezone.")
    return result


def _check_clock(checked_at, now, limit):
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise DataError("now must be a timezone-aware datetime.")
    if not isinstance(limit, timedelta) or limit <= timedelta(0):
        raise DataError("Freshness limit must be a positive timedelta.")
    if checked_at > now:
        raise ReviewBlocked("Records have a future check time.")
    if now - checked_at > limit:
        raise ReviewBlocked("Records are too old. Check them again before using the draft.")


def _validate(snapshot):
    if not isinstance(snapshot, dict):
        raise DataError("Snapshot must be an object.")
    if set(snapshot) != {"checked_at", "currency", "customers", "invoices"}:
        raise DataError("Snapshot fields do not match the demonstration format.")
    if snapshot["currency"] != "GBP":
        raise DataError("This demonstration supports GBP only.")
    checked_at = _timestamp(snapshot["checked_at"], "checked_at")
    if not isinstance(snapshot["customers"], list) or not isinstance(snapshot["invoices"], list):
        raise DataError("Customers and invoices must be lists.")
    customers = {}
    for customer in snapshot["customers"]:
        if not isinstance(customer, dict) or set(customer) != {"id", "name"}:
            raise DataError("Each customer needs exactly an id and name.")
        identifier = _text(customer["id"], "Customer id")
        if identifier in customers:
            raise DataError("Duplicate customer id.")
        customers[identifier] = _text(customer["name"], "Customer name")
    required = {"reference", "customer_id", "due_date", "gross_pence", "received_pence", "status"}
    optional = {"dispute_reason", "dispute_action", "last_payment_at"}
    references = set()
    invoices = []
    for invoice in snapshot["invoices"]:
        if not isinstance(invoice, dict) or not required <= set(invoice) or set(invoice) - required - optional:
            raise DataError("Invoice fields do not match the demonstration format.")
        reference = _text(invoice["reference"], "Invoice reference")
        if reference in references:
            raise DataError("Duplicate invoice reference.")
        references.add(reference)
        customer_id = _text(invoice["customer_id"], "Invoice customer id")
        if customer_id not in customers:
            raise DataError("Invoice refers to an unknown customer.")
        try:
            due_text = _text(invoice["due_date"], "Due date")
            due = date.fromisoformat(due_text)
            if due.isoformat() != due_text:
                raise ValueError("Use YYYY-MM-DD.")
        except ValueError as exc:
            raise DataError("Due date must use YYYY-MM-DD.") from exc
        gross, received = invoice["gross_pence"], invoice["received_pence"]
        if type(gross) is not int or type(received) is not int or gross <= 0 or not 0 <= received <= gross:
            raise DataError("Invoice money must be integer pence with 0 <= received <= gross.")
        status = invoice["status"]
        if not isinstance(status, str) or status not in {"open", "disputed", "paid", "factored"}:
            raise DataError("Unsupported invoice status; ask finance to check it.")
        if status == "paid" and gross != received:
            raise DataError("Paid status disagrees with the outstanding balance.")
        for key in optional & set(invoice):
            _text(invoice[key], key)
        if status == "disputed" and not {"dispute_reason", "dispute_action"} <= set(invoice):
            raise DataError("A disputed invoice needs a reason and an action owner.")
        if status != "disputed" and {"dispute_reason", "dispute_action"} & set(invoice):
            raise DataError("Dispute details disagree with the status; ask finance to check it.")
        if "last_payment_at" in invoice:
            payment_at = _timestamp(invoice["last_payment_at"], "last_payment_at")
            if received == 0 or payment_at > checked_at:
                raise DataError("Payment time or received amount is inconsistent with the snapshot.")
        invoices.append((invoice, due))
    return checked_at, customers, invoices


def review_customer(snapshot, customer_id, now, *, freshness_limit=timedelta(minutes=10)):
    """Review one customer's snapshot. The fixed demo freshness rule is configurable."""
    checked_at, customers, invoices = _validate(snapshot)
    _check_clock(checked_at, now, freshness_limit)
    _text(customer_id, "Requested customer id")
    if customer_id not in customers:
        raise DataError("Requested customer does not exist.")
    selected = sorted((item for item in invoices if item[0]["customer_id"] == customer_id),
                      key=lambda item: item[0]["reference"])
    review_date = now.astimezone(timezone.utc).date()
    decisions, eligible = [], []
    for invoice, due in selected:
        balance = invoice["gross_pence"] - invoice["received_pence"]
        status = invoice["status"]
        if balance == 0:
            action, explanation = "PAID", "Nothing to request."
        elif status == "disputed":
            action = "COLLEAGUE ACTION"
            explanation = f"{invoice['dispute_reason']} {invoice['dispute_action']}"
        elif status == "factored":
            action, explanation = "FACTOR CHECK", "Finance checks with the invoice-finance provider; no direct chaser."
        elif due >= review_date:
            action, explanation = "NOT OVERDUE", f"Due {due:%d %b %Y}; no overdue payment request."
        else:
            action, explanation = "RAISE ON CALL", f"Overdue since {due:%d %b %Y}."
            eligible.append((invoice["reference"], balance))
        decisions.append(Decision(invoice["reference"], balance, action, explanation))
    total = sum(amount for _, amount in eligible)
    draft = None
    if eligible:
        items = (f"invoice {eligible[0][0]}" if len(eligible) == 1 else
                 "; ".join(f"invoice {reference} ({money(amount)})" for reference, amount in eligible))
        draft = (f"Hello, could you confirm when we can expect payment of {money(total)} "
                 f"for {items}? Thank you.")
    # Capture immutable record values. Other customers do not invalidate this customer's draft.
    signature = (customers[customer_id], tuple(tuple(sorted(invoice.items())) for invoice, _ in selected))
    return Review(customer_id, customers[customer_id], checked_at, freshness_limit,
                  tuple(decisions), total, draft, signature)


def assert_current(review, latest_snapshot, now):
    """Block stale/changed evidence. Passing still requires a human finance review."""
    _check_clock(review.checked_at, now, review.freshness_limit)
    latest = review_customer(latest_snapshot, review.customer_id, now,
                             freshness_limit=review.freshness_limit)
    if latest.checked_at < review.checked_at:
        raise ReviewBlocked("The supplied records are older than the review.")
    if latest._signature != review._signature or latest.draft != review.draft:
        raise ReviewBlocked("Customer records changed. Replace the old draft and ask finance to review it.")


def load_snapshot(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    folder = Path(__file__).resolve().parent / "data"
    first = load_snapshot(folder / "first-review.json")
    after = load_snapshot(folder / "after-payment.json")
    render(first, after, "CUSTOMER-001")


def render(first, after, customer_id):
    first_time = _timestamp(first["checked_at"], "checked_at")
    later_time = _timestamp(after["checked_at"], "checked_at")
    review = review_customer(first, customer_id, first_time)
    refreshed = review_customer(after, customer_id, later_time)
    print("CREDIT CONTROL BEFORE A CUSTOMER CALL")
    print("Fictional records | GBP | No live connection or email sending")
    print(f"Customer: {review.customer_name} ({review.customer_id})")
    print(f"Records checked: {review.checked_at.astimezone(timezone.utc):%d %b %Y, %H:%M UTC}")
    print("Demo freshness limit: 10 minutes; recheck before using a draft.")
    refs = [d.reference for d in review.decisions if d.action == "RAISE ON CALL"]
    print(f"Raise on the call: {', '.join(refs) or 'none'}, {money(review.amount_to_raise_pence)}")
    print()
    for decision in review.decisions:
        print(f"{decision.reference} | {money(decision.outstanding_pence)} outstanding | {decision.action}")
        print(f"  {decision.explanation}")
    print("\nDRAFT FOR FINANCE REVIEW")
    print(review.draft or "No reminder required.")
    print("\nRECHECK BEFORE FINANCE REVIEW")
    prior = {row["reference"]: row["received_pence"] for row in first["invoices"]
             if row["customer_id"] == customer_id}
    for row in after["invoices"]:
        ref = row["reference"]
        if row["customer_id"] == customer_id and ref in prior:
            change = row["received_pence"] - prior[ref]
            if change > 0:
                print(f"{ref}: allocated receipts increased by {money(change)}.")
    print(f"Records checked again: {later_time.astimezone(timezone.utc):%d %b %Y, %H:%M UTC}")
    try:
        assert_current(review, after, later_time)
    except ReviewBlocked as exc:
        print(f"OLD DRAFT BLOCKED: {exc}")
    else:
        print("Earlier review still matches.")
    assert_current(refreshed, after, later_time)
    print(f"Revised amount to raise: {money(refreshed.amount_to_raise_pence)}")
    print("CURRENT DRAFT FOR FINANCE REVIEW")
    print(refreshed.draft or "No reminder required.")
    print("Finance still checks the balance, reference and recipient before any reminder is sent.")
    print("This example does not send messages or authorise sending.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
