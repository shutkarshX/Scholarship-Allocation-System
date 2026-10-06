import unittest

from app import app


class AllocationApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_allocation_api_returns_budget_result(self):
        response = self.client.get("/api/allocation?budget=100000")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["budget"], 100000)
        self.assertEqual(data["total_awarded"], 90000)
        self.assertEqual(data["total_value"], 257.0)
        self.assertEqual(
            {item["roll_no"] for item in data["selected"]},
            {"250133154002", "250133154004", "250133154008"},
        )
        self.assertTrue(data["cross_check_matches"])

    def test_allocation_api_rejects_invalid_budget(self):
        response = self.client.get("/api/allocation?budget=95500")
        self.assertEqual(response.status_code, 400)
        self.assertIn("multiple of ₹1,000", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
