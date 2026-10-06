"""Heap-based priority queue for scholarship applicant ranking."""

import heapq


class ScholarshipPriorityQueue:
    """Max-priority queue implemented with Python's min-heap."""

    def __init__(self) -> None:
        self._heap: list[tuple[float, str, dict]] = []

    def push(self, applicant: dict) -> None:
        """Add an eligible applicant to the priority queue."""
        if not applicant.get("eligible"):
            raise ValueError("Only eligible applicants can be ranked")

        if "priority_score" not in applicant:
            raise ValueError("Applicant must have a priority_score")

        roll_no = str(applicant.get("roll_no", ""))
        if not roll_no:
            raise ValueError("Applicant must have a roll_no")

        score = float(applicant["priority_score"])
        heapq.heappush(self._heap, (-score, roll_no, applicant))

    def pop(self) -> dict:
        """Remove and return the highest-priority applicant."""
        if not self._heap:
            raise IndexError("Priority queue is empty")

        _, _, applicant = heapq.heappop(self._heap)
        return applicant

    def peek(self) -> dict:
        """Return the highest-priority applicant without removing it."""
        if not self._heap:
            raise IndexError("Priority queue is empty")

        return self._heap[0][2]

    def __len__(self) -> int:
        return len(self._heap)

    def rank_all(self) -> list[dict]:
        """Return all queued applicants in descending priority order."""
        ranked = []

        while self._heap:
            applicant = self.pop()
            ranked.append(
                {
                    **applicant,
                    "rank": len(ranked) + 1,
                }
            )

        return ranked


def rank_eligible_applicants(applicants: list[dict]) -> list[dict]:
    """Rank eligible applicants using the heap-based priority queue."""
    queue = ScholarshipPriorityQueue()

    for applicant in applicants:
        if applicant.get("eligible"):
            queue.push(applicant)

    return queue.rank_all()
