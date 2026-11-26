import unittest
from review import assess, load


class VariationTests(unittest.TestCase):
    def setUp(self):
        self.docs = load("evidence.json")
        self.claims = load("interpretation.json")

    def check(self, day="2026-10-31"):
        return assess(self.docs, self.claims, day)

    def test_cutoff_replacement_and_prior_billing(self):
        self.assertEqual(self.check()[:2], (5300, 10))
        self.assertEqual(self.check("2026-11-03")[:2], (6150, 0))
        self.assertNotIn("I1", self.check()[2])
        self.assertNotIn("C2", self.check()[2])

    def test_site_email_cannot_certify(self):
        self.claims.append({"id":"E1","quote":"All 110 metres look fine to me.",
                            "fields":{"certified_m":110}})
        with self.assertRaisesRegex(ValueError, "Source cannot"):
            self.check()

    def test_omitted_revision_stops_review(self):
        self.claims = [c for c in self.claims if c["id"] != "I2"]
        with self.assertRaisesRegex(ValueError, "Missing extraction"):
            self.check()

    def test_invented_quote_stops_review(self):
        self.claims[0]["quote"] = "The full amount is approved."
        with self.assertRaisesRegex(ValueError, "citation"):
            self.check()
