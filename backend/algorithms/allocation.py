"""Budget-constrained scholarship allocation algorithms.

The model is an exact 0/1 allocation problem:
- eligible applicant = item
- requested amount = cost
- priority score = value
- budget = capacity
- each applicant is either fully funded or not funded
- objective = maximum total priority value without exceeding the budget.

For equal-value solutions, the deterministic tie-break is:
1. lower total spending;
2. lexicographically smaller sorted roll-number tuple.

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
    """Return True when solution A is preferred to solution B."""
    epsilon = 1e-9
    if value_a > value_b + epsilon:
        return True
    if abs(value_a - value_b) <= epsilon:
        if cost_a != cost_b:
            return cost_a < cost_b
        return tuple(sorted(rolls_a)) < tuple(sorted(rolls_b))
    return False


def allocate_dynamic_programming(applicants: list[dict], budget: int) -> AllocationResult:
    """Solve scholarship allocation exactly using 0/1 knapsack DP."""
    if budget < 0 or budget % BUDGET_UNIT != 0:
        raise ValueError("Budget must be a non-negative multiple of ₹1,000")

    items = _prepare_items(applicants)
    capacity = budget // BUDGET_UNIT
    n = len(items)

    # Each state stores: (value, cost, sorted roll numbers, selected indices).
    # Keeping the complete state makes equal-value tie-breaking explicit.
    empty_state = (0.0, 0, (), ())
    states = [[empty_state] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        for remaining in range(capacity + 1):
            best = states[i - 1][remaining]
            if item["cost"] <= remaining:
                previous = states[i - 1][remaining - item["cost"]]
                candidate = (
                    previous[0] + item["value"],
                    previous[1] + item["cost"],
                    tuple(sorted(previous[2] + (item["roll_no"],))),
                    previous[3] + (i - 1,),
                )
                if _better(candidate[0], candidate[1], candidate[2],
                           best[0], best[1], best[2]):
                    best = candidate
            states[i][remaining] = best

    best = states[n][capacity]
    selected_indices = best[3]
    selected = [items[index]["applicant"] for index in selected_indices]
    total_awarded = best[1] * BUDGET_UNIT

    return AllocationResult(
        selected=selected,
        total_awarded=total_awarded,
        total_value=round(best[0], 2),
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
        key=lambda item: (
            item["value"] / item["cost"] if item["cost"] else 0,
            item["value"],
            item["roll_no"],
        ),
        reverse=True,
    )

    best_value = 0.0
    best_cost = 0
    best_rolls = ()
    best_indices = ()

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
        nonlocal best_value, best_cost, best_rolls, best_indices

        chosen_rolls = tuple(sorted(ordered[i]["roll_no"] for i in chosen))
        if _better(
            value,
            cost,
            chosen_rolls,
            best_value,
            best_cost,
            best_rolls,
        ):
            best_value = value
            best_cost = cost
            best_rolls = chosen_rolls
            best_indices = chosen

        if index >= len(ordered) or bound(index, cost, value) < best_value - 1e-9:
            return

        item = ordered[index]
        if cost + item["cost"] <= capacity:
            search(
                index + 1,
                cost + item["cost"],
                value + item["value"],
                chosen + (index,),
            )
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
