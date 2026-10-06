import unittest

from algorithms.allocation import (
    allocate_branch_and_bound,
    allocate_dynamic_programming,
)


class AllocationTests(unittest.TestCase):
    def applicant(self, roll_no, amount, score, eligible=True):
        return {
            "roll_no": roll_no,
            "name": f"Applicant {roll_no}",
            "requested_amount": amount,
            "priority_score": score,
            "eligible": eligible,
        }

    def test_dp_respects_budget_and_maximizes_value(self):
        applicants = [
            self.applicant("1001", 30000, 60),
            self.applicant("1002", 20000, 45),
            self.applicant("1003", 10000, 30),
        ]
        result = allocate_dynamic_programming(applicants, 50000)
        self.assertEqual({a["roll_no"] for a in result.selected}, {"1001", "1002"})
        self.assertEqual(result.total_awarded, 50000)
        self.assertEqual(result.total_value, 105.0)

    def test_dp_excludes_ineligible_applicants(self):
        applicants = [
            self.applicant("1001", 20000, 90, eligible=False),
            self.applicant("1002", 20000, 50),
        ]
        result = allocate_dynamic_programming(applicants, 20000)
        self.assertEqual([a["roll_no"] for a in result.selected], ["1002"])

    def test_equal_value_prefers_lower_spending(self):
        applicants = [
            self.applicant("1001", 40000, 100),
            self.applicant("1002", 30000, 100),
            self.applicant("1003", 10000, 0),
        ]
        result = allocate_dynamic_programming(applicants, 40000)
        self.assertEqual([a["roll_no"] for a in result.selected], ["1002"])

    def test_equal_value_and_cost_uses_roll_number_tie_break(self):
        applicants = [
            self.applicant("1002", 20000, 50),
            self.applicant("1001", 20000, 50),
        ]
        result = allocate_dynamic_programming(applicants, 20000)
        self.assertEqual([a["roll_no"] for a in result.selected], ["1001"])

    def test_dp_and_branch_and_bound_match_on_tie_cases(self):
        applicants = [
            self.applicant("1004", 40000, 100),
            self.applicant("1002", 30000, 100),
            self.applicant("1001", 20000, 50),
        ]
        dp = allocate_dynamic_programming(applicants, 40000)
        bnb = allocate_branch_and_bound(applicants, 40000)
        self.assertEqual(dp.total_awarded, 30000)
        self.assertEqual(dp.total_value, 100.0)
        self.assertEqual(
            {a["roll_no"] for a in dp.selected},
            {a["roll_no"] for a in bnb.selected},
        )

    def test_branch_and_bound_matches_dp(self):
        applicants = [
            self.applicant("1001", 30000, 60),
            self.applicant("1002", 20000, 45),
            self.applicant("1003", 10000, 30),
            self.applicant("1004", 40000, 75),
        ]
        dp = allocate_dynamic_programming(applicants, 50000)
        bnb = allocate_branch_and_bound(applicants, 50000)
        self.assertEqual(bnb.total_awarded, dp.total_awarded)
        self.assertEqual(bnb.total_value, dp.total_value)
        self.assertEqual({a["roll_no"] for a in bnb.selected},
                         {a["roll_no"] for a in dp.selected})

    def test_zero_budget_allocates_nothing(self):
        result = allocate_dynamic_programming(
            [self.applicant("1001", 20000, 80)], 0
        )
        self.assertEqual(result.selected, [])
        self.assertEqual(result.total_awarded, 0)

    def test_no_applicant_fits(self):
        result = allocate_dynamic_programming(
            [self.applicant("1001", 30000, 80)], 20000
        )
        self.assertEqual(result.selected, [])
        self.assertEqual(result.total_awarded, 0)

    def test_budget_larger_than_all_requests(self):
        applicants = [
            self.applicant("1001", 20000, 80),
            self.applicant("1002", 30000, 70),
        ]
        result = allocate_dynamic_programming(applicants, 100000)
        self.assertEqual({a["roll_no"] for a in result.selected}, {"1001", "1002"})
        self.assertEqual(result.total_awarded, 50000)

    def test_branch_and_bound_zero_budget(self):
        result = allocate_branch_and_bound(
            [self.applicant("1001", 20000, 80)], 0
        )
        self.assertEqual(result.selected, [])
        self.assertEqual(result.total_awarded, 0)

    def test_branch_and_bound_no_applicant_fits(self):
        result = allocate_branch_and_bound(
            [self.applicant("1001", 30000, 80)], 20000
        )
        self.assertEqual(result.selected, [])
        self.assertEqual(result.total_awarded, 0)

    def test_budget_must_use_thousand_rupee_units(self):
        with self.assertRaises(ValueError):
            allocate_dynamic_programming(
                [self.applicant("1001", 20000, 80)], 25500
            )

    def test_requested_amount_must_use_thousand_rupee_units(self):
        with self.assertRaises(ValueError):
            allocate_dynamic_programming(
                [self.applicant("1001", 25500, 80)], 30000
            )


if __name__ == "__main__":
    unittest.main()
