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

    def test_genuine_quote_with_wrong_extracted_rate(self):
        self.claims[1]["fields"]["rate_gbp"] = 95
        with self.assertRaisesRegex(ValueError, "I2: verify the extracted rate"):
            self.check()

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

    def test_site_measure_cannot_replace_certified_quantity(self):
        certificate = next(c for c in self.claims if c["id"] == "C1")
        certificate["fields"]["certified_m"] = 110
        with self.assertRaisesRegex(ValueError, "C1: verify the certified quantity"):
            self.check()

    def test_other_extracted_values_must_agree_with_their_sources(self):
        for ref, field in (("I2", "limit_m"), ("D1", "measured_m"), ("B1", "billed_gbp")):
            with self.subTest(ref=ref):
                self.claims = load("interpretation.json")
                next(row for row in self.claims if row["id"] == ref)["fields"][field] += 1
                with self.assertRaisesRegex(ValueError, ref):
                    self.check()

    def test_later_bad_certificate_cannot_change_issued_october_result(self):
        next(c for c in self.claims if c["id"] == "C2")["fields"]["certified_m"] = 109
        self.assertEqual(self.check()[:2], (5300, 10))
        with self.assertRaisesRegex(ValueError, "C2"):
            self.check("2026-11-03")
