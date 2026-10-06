"""Budget-constrained scholarship allocation algorithms.

The model is an exact 0/1 allocation problem:
- eligible applicant = item
- requested amount = cost
- priority score = value
- budget = capacity
- each applicant is either fully funded or not funded
- objective is maximum total priority value without exceeding budget.

The dynamic-programming solver is the primary allocation algorithm.
The branch-and-bound solver independently solves the same model for verification.
"""

from __future__ import annotations

from dataclasses import dataclass

BUDGET_UNIT = 1000


@dataclass(frozen=True)
class AllocationResult:
    selected: list[dict]
    total_awarded: int
    total_value: float
    remaining_budget: int


def _prepare_items(applicants: list[dict]) -> list[dict]:
    items = []
    for applicant in applicants:
        if not applicant.get("eligible"):
            continue

        amount = float(applicant.get("requested_amount", 0))
        if amount <= 0 or amount % BUDGET_UNIT != 0:
            raise ValueError("Requested amounts must be positive multiples of ₹1,000")

        items.append(
            {
                "applicant": applicant,
                "cost": int(amount // BUDGET_UNIT),
                "value": float(applicant.get("priority_score", 0)),
                "roll_no": str(applicant.get("roll_no", "")),
            }
        )
    return items


def _better(value_a, cost_a, rolls_a, value_b, cost_b, rolls_b):
    epsilon = 1e-9
    if value_a > value_b + epsilon:
        return True
    if abs(value_a - value_b) <= epsilon:
        if cost_a < cost_b:
            return True
        if cost_a == cost_b:
            return rolls_a < rolls_b
    return False


def allocate_dynamic_programming(applicants: list[dict], budget: int) -> AllocationResult:
    """Solve scholarship allocation exactly using 0/1 knapsack DP."""
    if budget < 0 or budget % BUDGET_UNIT != 0:
        raise ValueError("Budget must be a non-negative multiple of ₹1,000")

    items = _prepare_items(applicants)
    capacity = budget // BUDGET_UNIT
    n = len(items)

    values = [[0.0] * (capacity + 1) for _ in range(n + 1)]
    choices = [[False] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        for remaining in range(capacity + 1):
            best = values[i - 1][remaining]
            if item["cost"] <= remaining:
                candidate = values[i - 1][remaining - item["cost"]] + item["value"]
                if candidate > best + 1e-9:
                    values[i][remaining] = candidate
                    choices[i][remaining] = True
                    continue
            values[i][remaining] = best

    selected_indices = []
    remaining = capacity
    for i in range(n, 0, -1):
        if choices[i][remaining]:
            selected_indices.append(i - 1)
            remaining -= items[i - 1]["cost"]

    selected_indices.reverse()
    selected = [items[index]["applicant"] for index in selected_indices]
    total_awarded = sum(items[index]["cost"] * BUDGET_UNIT for index in selected_indices)
    total_value = sum(items[index]["value"] for index in selected_indices)

    return AllocationResult(
        selected=selected,
        total_awarded=total_awarded,
        total_value=round(total_value, 2),
        remaining_budget=budget - total_awarded,
    )


def allocate_branch_and_bound(applicants: list[dict], budget: int) -> AllocationResult:
    """Solve the same 0/1 allocation problem with branch-and-bound."""
    if budget < 0 or budget % BUDGET_UNIT != 0:
        raise ValueError("Budget must be a non-negative multiple of ₹1,000")

    items = _prepare_items(applicants)
    capacity = budget // BUDGET_UNIT

    ordered = sorted(
        items,
        key=lambda item: item["value"] / item["cost"] if item["cost"] else 0,
        reverse=True,
    )

    best_value = 0.0
    best_cost = 0
    best_indices = ()

    def roll_tuple(indices):
        return tuple(ordered[i]["roll_no"] for i in indices)

    def bound(start, cost, value):
        if cost >= capacity:
            return value
        estimate = value
        used = cost
        for index in range(start, len(ordered)):
            item = ordered[index]
            if used + item["cost"] <= capacity:
                used += item["cost"]
                estimate += item["value"]
            else:
                available = capacity - used
                if item["cost"] > 0:
                    estimate += item["value"] * (available / item["cost"])
                break
        return estimate

    def search(index, cost, value, chosen):
        nonlocal best_value, best_cost, best_indices

        if _better(value, cost, roll_tuple(chosen),
                   best_value, best_cost, roll_tuple(best_indices)):
            best_value = value
            best_cost = cost
            best_indices = chosen

        if index >= len(ordered) or bound(index, cost, value) < best_value - 1e-9:
            return

        item = ordered[index]
        if cost + item["cost"] <= capacity:
            search(index + 1, cost + item["cost"],
                   value + item["value"], chosen + (index,))
        search(index + 1, cost, value, chosen)

    search(0, 0, 0.0, ())

    selected = [ordered[index]["applicant"] for index in best_indices]
    total_awarded = best_cost * BUDGET_UNIT

    return AllocationResult(
        selected=selected,
        total_awarded=total_awarded,
        total_value=round(best_value, 2),
        remaining_budget=budget - total_awarded,
    )
