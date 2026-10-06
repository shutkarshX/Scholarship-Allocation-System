"""Tests for the hash-based applicant lookup API."""

import unittest

from app import app


class ApplicantLookupApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_lookup_returns_applicant_by_roll_number(self) -> None:
        response = self.client.get("/api/applicants/250133154001")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["roll_no"], "250133154001")
        self.assertEqual(data["name"], "Aarav Sharma")

    def test_rankings_return_eligible_applicants_in_priority_order(self) -> None:
        response = self.client.get("/api/rankings")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data)
        self.assertEqual([item["rank"] for item in data], list(range(1, len(data) + 1)))
        self.assertEqual(
            data,
            sorted(data, key=lambda item: (-item["priority_score"], item["roll_no"])),
        )
        self.assertTrue(all(item["eligible"] for item in data))

    def test_lookup_returns_404_for_unknown_roll_number(self) -> None:
        response = self.client.get("/api/applicants/does-not-exist")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Applicant not found")


if __name__ == "__main__":
    unittest.main()
