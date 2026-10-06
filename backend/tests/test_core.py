import json
import tempfile
import unittest
from pathlib import Path

from algorithms.hashing import ApplicantHashTable
from algorithms.scoring import calculate_priority_score, calculate_need_score
from services.applicant_store import ApplicantStore
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
            "category": "General",
            "dependents": 3,
            "previous_scholarship": False,
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

    def test_applicant_store_adds_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "students.json"
            data_file.write_text("[]", encoding="utf-8")
            store = ApplicantStore(data_file)

            store.add(self.applicant)

            records = json.loads(data_file.read_text(encoding="utf-8"))
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["roll_no"], "TEST001")

    def test_applicant_store_rejects_duplicate_roll_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "students.json"
            data_file.write_text(json.dumps([self.applicant]), encoding="utf-8")
            store = ApplicantStore(data_file)

            with self.assertRaises(ValueError):
                store.add({**self.applicant, "name": "Another Applicant"})


if __name__ == "__main__":
    unittest.main()
