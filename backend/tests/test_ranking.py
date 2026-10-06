import unittest

from algorithms.ranking import ScholarshipPriorityQueue, rank_eligible_applicants


class RankingTests(unittest.TestCase):
    def applicant(self, roll_no, score, eligible=True):
        return {
            "roll_no": roll_no,
            "name": f"Applicant {roll_no}",
            "eligible": eligible,
            "priority_score": score,
        }

    def test_highest_priority_is_returned_first(self):
        queue = ScholarshipPriorityQueue()
        queue.push(self.applicant("1002", 82.5))
        queue.push(self.applicant("1001", 91.0))

        self.assertEqual(queue.peek()["roll_no"], "1001")
        self.assertEqual(queue.pop()["roll_no"], "1001")

    def test_rank_order_is_descending(self):
        applicants = [
            self.applicant("1001", 72.0),
            self.applicant("1002", 94.0),
            self.applicant("1003", 81.5),
        ]

        ranked = rank_eligible_applicants(applicants)

        self.assertEqual(
            [item["roll_no"] for item in ranked],
            ["1002", "1003", "1001"],
        )
        self.assertEqual([item["rank"] for item in ranked], [1, 2, 3])

    def test_ineligible_applicants_are_excluded(self):
        applicants = [
            self.applicant("1001", 95.0, eligible=False),
            self.applicant("1002", 80.0),
        ]

        ranked = rank_eligible_applicants(applicants)

        self.assertEqual([item["roll_no"] for item in ranked], ["1002"])

    def test_equal_scores_use_roll_number_as_tie_breaker(self):
        applicants = [
            self.applicant("1007", 85.0),
            self.applicant("1002", 85.0),
        ]

        ranked = rank_eligible_applicants(applicants)

        self.assertEqual(
            [item["roll_no"] for item in ranked],
            ["1002", "1007"],
        )

    def test_empty_input(self):
        self.assertEqual(rank_eligible_applicants([]), [])

    def test_single_applicant(self):
        ranked = rank_eligible_applicants([self.applicant("1001", 88.0)])

        self.assertEqual(ranked[0]["roll_no"], "1001")
        self.assertEqual(ranked[0]["rank"], 1)

    def test_ineligible_applicant_cannot_be_added_directly(self):
        queue = ScholarshipPriorityQueue()

        with self.assertRaises(ValueError):
            queue.push(self.applicant("1001", 90.0, eligible=False))

    def test_missing_priority_score_is_rejected(self):
        queue = ScholarshipPriorityQueue()

        with self.assertRaises(ValueError):
            queue.push(
                {
                    "roll_no": "1001",
                    "eligible": True,
                }
            )

    def test_empty_queue_pop_and_peek(self):
        queue = ScholarshipPriorityQueue()

        with self.assertRaises(IndexError):
            queue.pop()

        with self.assertRaises(IndexError):
            queue.peek()


if __name__ == "__main__":
    unittest.main()
