"""Hash-table based applicant lookup."""


class ApplicantHashTable:
    """Simple wrapper around a Python hash table for average O(1) lookup."""

    def __init__(self) -> None:
        self._table: dict[str, dict] = {}

    def insert(self, applicant: dict) -> None:
        roll_no = applicant.get("roll_no")
        if not roll_no:
            raise ValueError("Applicant must have a roll_no")
        self._table[str(roll_no)] = applicant

    def get(self, roll_no: str) -> dict | None:
        return self._table.get(str(roll_no))

    def contains(self, roll_no: str) -> bool:
        return str(roll_no) in self._table

    def remove(self, roll_no: str) -> dict | None:
        return self._table.pop(str(roll_no), None)

    def __len__(self) -> int:
        return len(self._table)
