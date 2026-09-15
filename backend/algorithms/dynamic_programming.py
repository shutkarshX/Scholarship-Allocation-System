"""0/1 Knapsack-style dynamic programming allocation."""


def dp_allocate(applicants: list[dict], budget: int) -> dict:
    """Find an optimal subset under the integer budget constraint.

    Objective: maximize total applicant priority score while total requested
    scholarship amount stays within the available budget.
    """
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    candidates = [
        a for a in applicants
        if a.get("eligible", True) and int(a.get("requested_amount", 0)) > 0
    ]
    n = len(candidates)

    # dp[w] stores the best total priority value achievable with budget w.
    dp = [0.0] * (budget + 1)
    choices: list[list[int]] = [[] for _ in range(budget + 1)]

    for index, applicant in enumerate(candidates):
        cost = int(applicant["requested_amount"])
        value = float(applicant.get("priority_score", 0))

        for w in range(budget, cost - 1, -1):
            candidate_value = dp[w - cost] + value
            if candidate_value > dp[w]:
                dp[w] = candidate_value
                choices[w] = choices[w - cost] + [index]

    selected = [
        {"applicant": candidates[i], "amount": int(candidates[i]["requested_amount"])}
        for i in choices[budget]
    ]
    budget_used = sum(item["amount"] for item in selected)

    return {
        "method": "dynamic_programming",
        "selected": selected,
        "budget_used": budget_used,
        "remaining_budget": budget - budget_used,
        "total_value": round(dp[budget], 2),
        "candidate_count": n,
    }
