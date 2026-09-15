"""Sorting algorithms used for applicant ranking."""


def merge_sort(applicants: list[dict]) -> list[dict]:
    """Return applicants sorted by priority score descending.

    Ties are broken by higher financial need score, then roll number.
    """
    if len(applicants) <= 1:
        return applicants.copy()

    midpoint = len(applicants) // 2
    left = merge_sort(applicants[:midpoint])
    right = merge_sort(applicants[midpoint:])
    return _merge(left, right)


def _key(applicant: dict) -> tuple:
    return (
        applicant.get("priority_score", 0),
        applicant.get("need_score", 0),
        applicant.get("roll_no", ""),
    )


def _merge(left: list[dict], right: list[dict]) -> list[dict]:
    result: list[dict] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if _key(left[i]) >= _key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
