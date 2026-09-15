"""Greedy scholarship allocation."""


def allocation_value(applicant: dict) -> float:
    """Return the benefit value used by the allocation algorithms."""
    return float(applicant.get("priority_score", 0))


def greedy_allocate(applicants: list[dict], budget: int) -> dict:
    """Allocate requested amounts by highest value-per-rupee first.

    This is a heuristic and is intentionally compared with dynamic programming.
    """
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    candidates = [a for a in applicants if a.get("eligible", True)]
    candidates = [a for a in candidates if int(a.get("requested_amount", 0)) > 0]
    candidates.sort(
        key=lambda a: (
            allocation_value(a) / int(a["requested_amount"]),
            allocation_value(a),
        ),
        reverse=True,
    )

    selected: list[dict] = []
    remaining = budget
    total_value = 0.0

    for applicant in candidates:
        amount = int(applicant["requested_amount"])
        if amount <= remaining:
            selected.append({"applicant": applicant, "amount": amount})
            remaining -= amount
            total_value += allocation_value(applicant)

    return {
        "method": "greedy",
        "selected": selected,
        "budget_used": budget - remaining,
        "remaining_budget": remaining,
        "total_value": round(total_value, 2),
    }
