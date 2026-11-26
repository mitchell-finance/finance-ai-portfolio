"""Run from this directory: python -m unittest -v"""

from copy import deepcopy
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

from credit_review import DataError, ReviewBlocked, assert_current, load_snapshot, review_customer


class CreditReviewTests(unittest.TestCase):
    def setUp(self):
        data = Path(__file__).resolve().parent / "data"
        self.first = load_snapshot(data / "first-review.json")
        self.after = load_snapshot(data / "after-payment.json")
        self.now = datetime.fromisoformat("2026-11-26T09:00:00+00:00")
        self.later = self.now + timedelta(minutes=6)
        self.customer = "CUSTOMER-001"

    def review(self, snapshot=None, now=None, **kwargs):
        return review_customer(self.first if snapshot is None else snapshot,
                               self.customer, self.now if now is None else now, **kwargs)

    def test_only_unrestricted_overdue_amount_enters_draft(self):
        review = self.review()
        self.assertEqual(review.amount_to_raise_pence, 120000)
        self.assertIn("£1,200.00", review.draft)
        self.assertIn("DEMO-101", review.draft)
        for reference in ("DEMO-102", "DEMO-103", "DEMO-104", "DEMO-105"):
            self.assertNotIn(reference, review.draft)
        actions = {item.reference: item.action for item in review.decisions}
        self.assertEqual(actions, {
            "DEMO-101": "RAISE ON CALL", "DEMO-102": "COLLEAGUE ACTION",
            "DEMO-103": "PAID", "DEMO-104": "FACTOR CHECK", "DEMO-105": "NOT OVERDUE"})
        dispute = review.decisions[1].explanation
        self.assertIn("agreed quantity", dispute)
        self.assertIn("signed job record", dispute)
        self.assertIn("account manager", dispute)

    def test_late_partial_payment_blocks_old_draft_and_reduces_replacement(self):
        original = self.review()
        with self.assertRaisesRegex(ReviewBlocked, "records changed"):
            assert_current(original, self.after, self.later)
        updated = self.review(self.after, self.later)
        self.assertEqual(updated.amount_to_raise_pence, 70000)
        self.assertIn("£700.00", updated.draft)
        self.assertNotIn("£1,200.00", updated.draft)
        assert_current(updated, self.after, self.later)

    def test_full_payment_blocks_old_draft_and_removes_request(self):
        original = self.review()
        self.after["invoices"][0].update(received_pence=120000, status="paid")
        with self.assertRaises(ReviewBlocked):
            assert_current(original, self.after, self.later)
        updated = self.review(self.after, self.later)
        self.assertEqual(updated.amount_to_raise_pence, 0)
        self.assertIsNone(updated.draft)
        self.assertEqual(updated.decisions[0].action, "PAID")

    def test_other_customers_do_not_enter_or_invalidate_this_draft(self):
        self.first["customers"].append({"id": "CUSTOMER-002", "name": "Another Example Ltd"})
        foreign = deepcopy(self.first["invoices"][0])
        foreign.update(reference="OTHER-001", customer_id="CUSTOMER-002", gross_pence=900000)
        self.first["invoices"].append(foreign)
        original = self.review()
        self.assertEqual(len(original.decisions), 5)
        self.assertEqual(original.amount_to_raise_pence, 120000)
        self.assertNotIn("OTHER-001", original.draft)
        foreign["received_pence"] = 20000
        assert_current(original, self.first, self.now)

    def test_due_today_is_not_overdue(self):
        self.first["invoices"][0]["due_date"] = "2026-11-26"
        review = self.review()
        self.assertEqual(review.decisions[0].action, "NOT OVERDUE")
        self.assertIsNone(review.draft)

    def test_due_date_uses_utc_for_the_same_instant_with_different_offsets(self):
        self.first["invoices"][0]["due_date"] = "2026-11-25"
        utc_review = self.review()
        same_instant = self.now.astimezone(timezone(timedelta(hours=-12)))
        self.assertEqual(same_instant.date().isoformat(), "2026-11-25")
        offset_review = self.review(now=same_instant)
        self.assertEqual(utc_review.decisions, offset_review.decisions)
        self.assertEqual(utc_review.draft, offset_review.draft)
        self.assertEqual(offset_review.amount_to_raise_pence, 120000)

    def test_dispute_details_with_non_disputed_status_fail_closed(self):
        for status in ("open", "paid", "factored"):
            for field in ("dispute_reason", "dispute_action"):
                with self.subTest(status=status, field=field):
                    snapshot = deepcopy(self.first)
                    invoice = snapshot["invoices"][0]
                    invoice["status"] = status
                    if status == "paid":
                        invoice["received_pence"] = invoice["gross_pence"]
                    invoice[field] = "Office colleague checks the quantity query."
                    with self.assertRaisesRegex(DataError, "Dispute details disagree"):
                        self.review(snapshot)

    def test_old_snapshots_and_old_drafts_are_blocked(self):
        original = self.review()
        expired = self.now + timedelta(minutes=10, seconds=1)
        with self.assertRaisesRegex(ReviewBlocked, "too old"):
            self.review(now=expired)
        with self.assertRaisesRegex(ReviewBlocked, "too old"):
            assert_current(original, self.after, expired)
        self.review(now=self.now + timedelta(minutes=10))
        with self.assertRaises(ReviewBlocked):
            self.review(now=self.now + timedelta(minutes=3), freshness_limit=timedelta(minutes=2))

    def test_future_snapshots_and_naive_times_are_rejected(self):
        with self.assertRaisesRegex(ReviewBlocked, "future"):
            self.review(self.after, self.now)
        with self.assertRaises(DataError):
            self.review(now=self.now.replace(tzinfo=None))
        self.first["checked_at"] = "2026-11-26T09:00:00"
        with self.assertRaises(DataError):
            self.review()

    def test_older_supplied_records_cannot_replace_newer_review(self):
        newer = deepcopy(self.first)
        newer["checked_at"] = "2026-11-26T09:06:00+00:00"
        review = self.review(newer, self.later)
        with self.assertRaisesRegex(ReviewBlocked, "older than"):
            assert_current(review, self.first, self.later)

    def test_invalid_money_and_unsupported_status_fail_closed(self):
        changes = [
            {"received_pence": -1}, {"received_pence": 120001},
            {"gross_pence": 0}, {"gross_pence": "120000"},
            {"received_pence": 0.5}, {"received_pence": True},
            {"status": "paid"}, {"status": "unrecognised"}, {"status": []},
        ]
        for change in changes:
            with self.subTest(change=change):
                snapshot = deepcopy(self.first)
                snapshot["invoices"][0].update(change)
                with self.assertRaises(DataError):
                    self.review(snapshot)

    def test_missing_conflicting_or_malformed_records_fail_closed(self):
        snapshots = []
        bad = deepcopy(self.first)
        del bad["invoices"][1]["dispute_action"]
        snapshots.append(bad)
        bad = deepcopy(self.first)
        bad["invoices"].append(deepcopy(bad["invoices"][0]))
        snapshots.append(bad)
        for field, value in (("customer_id", "MISSING"), ("due_date", "31/11/2026")):
            bad = deepcopy(self.first)
            bad["invoices"][0][field] = value
            snapshots.append(bad)
        bad = deepcopy(self.after)
        bad["invoices"][0]["last_payment_at"] = "2026-11-26T09:07:00+00:00"
        snapshots.append(bad)
        bad = deepcopy(self.first)
        bad["currency"] = "USD"
        snapshots.append(bad)
        for snapshot in snapshots:
            with self.subTest(snapshot=snapshot), self.assertRaises(DataError):
                self.review(snapshot, self.later)

    def test_customer_details_or_dispute_change_requires_another_review(self):
        original = self.review()
        for changed in ("customer", "dispute"):
            with self.subTest(changed=changed):
                snapshot = deepcopy(self.first)
                if changed == "customer":
                    snapshot["customers"][0]["name"] = "Updated Example Ltd"
                else:
                    snapshot["invoices"][1]["dispute_reason"] = "Customer now disputes the rate."
                with self.assertRaises(ReviewBlocked):
                    assert_current(original, snapshot, self.now)

    def test_review_cannot_be_changed_by_mutating_inputs(self):
        review = self.review()
        self.first["invoices"][0]["received_pence"] = 50000
        self.assertEqual(review.amount_to_raise_pence, 120000)
        with self.assertRaises(FrozenInstanceError):
            review.amount_to_raise_pence = 70000
        with self.assertRaises(FrozenInstanceError):
            review.decisions[0].action = "PAID"
        with self.assertRaises(ReviewBlocked):
            assert_current(review, self.first, self.now)


if __name__ == "__main__":
    unittest.main()
