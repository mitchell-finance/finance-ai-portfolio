import unittest
from order_events import EVENTS, forecast


class OrderTests(unittest.TestCase):
    def test_out_of_order_duplicate_and_other_deal(self):
        for rows in (EVENTS, list(reversed(EVENTS))):
            self.assertEqual(forecast("OP17",48000,rows), (16000,32000))

    def test_newer_cancellation_reopens_value(self):
        self.assertEqual(forecast("OP17",48000,EVENTS+[("M04","OP17","PO8",3,0)]),(0,48000))

    def test_conflicting_message_or_revision_held(self):
        for ref in ("M02","NEW"):
            with self.assertRaises(ValueError):
                forecast("OP17",48000,EVENTS+[(ref,"OP17","PO8",2,20000)])
