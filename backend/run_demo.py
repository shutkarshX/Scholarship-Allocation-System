"""Run a small end-to-end demonstration of the DSA core."""

import json
from pathlib import Path

from algorithms.dynamic_programming import dp_allocate
from algorithms.greedy import greedy_allocate
from algorithms.hashing import ApplicantHashTable
from algorithms.scoring import (
    calculate_need_score,
    calculate_priority_score,
)
from algorithms.sorting import merge_sort
from algorithms.heap import MaxHeap


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "sample_students.json"
BUDGET = 100_000


def prepare_applicants() -> list[dict]:
    applicants = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for applicant in applicants:
        applicant["need_score"] = calculate_need_score(applicant["family_income"])
        applicant["priority_score"] = calculate_priority_score(
            applicant["cgpa"],
            applicant["family_income"],
            applicant["attendance"],
        )
    return applicants


def main() -> None:
    applicants = prepare_applicants()

    # Hashing: average O(1) lookup by roll number.
    table = ApplicantHashTable()
    for applicant in applicants:
        table.insert(applicant)

    # Merge sort: complete ranking by priority.
    ranked = merge_sort(applicants)

    # Max heap: repeatedly retrieve the highest-priority applicant.
    heap = MaxHeap()
    for applicant in applicants:
        heap.push(applicant)
    heap_order = [heap.pop() for _ in range(len(heap))]

    greedy = greedy_allocate(applicants, BUDGET)
    optimal = dp_allocate(applicants, BUDGET)

    print("=== Intelligent Scholarship Allocation System ===")
    print(f"Applicants: {len(applicants)}")
    print(f"Budget: ₹{BUDGET:,}")
    print("\nRanking (Merge Sort):")
    for rank, applicant in enumerate(ranked, start=1):
        print(f"{rank}. {applicant['name']} — {applicant['priority_score']}")

    print("\nTop applicant (Max Heap):")
    print(f"{heap_order[0]['name']} — {heap_order[0]['priority_score']}")

    print("\nHash lookup:")
    sample_roll = applicants[0]["roll_no"]
    print(f"{sample_roll} → {table.get(sample_roll)['name']}")

    print("\nAllocation comparison:")
    print(f"Greedy: {len(greedy['selected'])} selected, ₹{greedy['budget_used']:,} used, value {greedy['total_value']}")
    print(f"DP:     {len(optimal['selected'])} selected, ₹{optimal['budget_used']:,} used, value {optimal['total_value']}")


if __name__ == "__main__":
    main()
