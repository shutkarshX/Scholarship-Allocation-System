import unittest

from algorithms.hashing import ApplicantHashTable
from algorithms.scoring import calculate_priority_score, calculate_need_score
from services.eligibility import evaluate_eligibility


class CoreAlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.applicant = {
            "roll_no": "TEST001",
            "name": "Test Applicant",
            "course": "BTech CSE(DS)",
            "year": 3,
            "cgpa": 8.0,
            "attendance": 80,
            "family_income": 200000,
            "requested_amount": 25000,
        }

    def test_eligible_applicant(self):
        result = evaluate_eligibility(self.applicant)
        self.assertTrue(result["eligible"])

    def test_low_attendance_is_ineligible(self):
        applicant = {**self.applicant, "attendance": 74.9}
        result = evaluate_eligibility(applicant)
        self.assertFalse(result["eligible"])

    def test_income_threshold_is_inclusive(self):
        applicant = {**self.applicant, "family_income": 500000}
        result = evaluate_eligibility(applicant)
        self.assertTrue(result["eligible"])

    def test_income_above_threshold_is_ineligible(self):
        applicant = {**self.applicant, "family_income": 500001}
        result = evaluate_eligibility(applicant)
        self.assertFalse(result["eligible"])

    def test_score_weights(self):
        score = calculate_priority_score(10, 0, 100)
        self.assertEqual(score, 100.0)

    def test_need_score(self):
        self.assertEqual(calculate_need_score(250000), 50.0)

    def test_hash_lookup(self):
        table = ApplicantHashTable()
        table.insert(self.applicant)
        self.assertEqual(table.get("TEST001")["name"], "Test Applicant")
        self.assertIsNone(table.get("MISSING"))


if __name__ == "__main__":
    unittest.main()
