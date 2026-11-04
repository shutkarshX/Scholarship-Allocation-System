import json
import tempfile
import unittest
from pathlib import Path

from algorithms.hashing import ApplicantHashTable
from algorithms.scoring import calculate_priority_score, calculate_need_score
from services.applicant_store import ApplicantStore
from services.eligibility import evaluate_eligibility, validate_applicant


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

    def test_year_must_be_positive_integer(self):
        for year in (0, -1, 2.5):
            with self.subTest(year=year):
                errors = validate_applicant({**self.applicant, "year": year})
                self.assertIn("Year must be a positive integer", errors)

    def test_dependents_must_be_non_negative_integer(self):
        for dependents in (-1, 1.5):
            with self.subTest(dependents=dependents):
                errors = validate_applicant(
                    {**self.applicant, "dependents": dependents}
                )
                self.assertIn(
                    "Dependents must be a non-negative integer", errors
                )

    def test_dependents_are_required(self):
        applicant = {**self.applicant}
        del applicant["dependents"]
        self.assertIn(
            "Missing required field: dependents",
            validate_applicant(applicant),
        )

    def test_requested_amount_must_use_thousand_rupee_units(self):
        errors = validate_applicant(
            {**self.applicant, "requested_amount": 25500}
        )
        self.assertIn(
            "Requested scholarship amount must be a multiple of ₹1,000",
            errors,
        )

    def test_non_finite_numeric_values_are_rejected(self):
        errors = validate_applicant(
            {**self.applicant, "cgpa": float("nan")}
        )
        self.assertIn("CGPA must be a finite number", errors)

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
