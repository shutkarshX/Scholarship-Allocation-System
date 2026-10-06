"""Local JSON storage for applicant records used in the current phase."""

import json
from pathlib import Path


class ApplicantStore:
    """Read and append applicant records in the controlled local dataset."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    def load(self) -> list[dict]:
        return json.loads(self.data_file.read_text(encoding="utf-8"))

    def add(self, applicant: dict) -> None:
        applicants = self.load()
        roll_no = str(applicant["roll_no"])

        if any(str(existing["roll_no"]) == roll_no for existing in applicants):
            raise ValueError("An applicant with this roll number already exists")

        applicants.append(applicant)
        self.data_file.write_text(
            json.dumps(applicants, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
