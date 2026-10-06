# Review 2 Implementation Record

This record covers the actual Unit 3 and Unit 4 implementation for the second college review. It is separate from the earlier project-development Phase 2 checkpoint, which covered heap-based ranking.

## Unit 3 — Dynamic Programming

The scholarship allocation problem is modelled as a 0/1 knapsack problem.

- Applicant = item
- Requested scholarship amount = cost/weight
- Priority score = value
- Available scholarship budget = capacity
- Each applicant can be selected at most once.
- Selected applicants receive their full requested amount.
- Objective = maximize total priority score without exceeding the budget.

The primary implementation is backend/algorithms/allocation.py in allocate_dynamic_programming. The DP table evaluates applicants against budget capacities in ₹1,000 units and reconstructs the selected applicant set.

## Unit 4 — Branch and Bound

A branch-and-bound implementation solves the same 0/1 allocation model independently. It branches on selecting or skipping an applicant and uses a fractional upper bound to prune branches that cannot improve the current best solution.

It is used as an independent exact cross-check for the DP result.

## Allocation Policy Assumptions

These are project assumptions, not official institutional scholarship rules:

1. Only already-eligible applicants enter allocation.
2. Awards are full-request only; partial awards are not used.
3. An applicant is selected at most once.
4. The budget is fixed for an allocation run.
5. No category quota or institutional reservation rule is imposed by this project.
6. Priority score is the optimization value.
7. Equal total value prefers lower spending; if still tied, deterministic roll-number ordering is used.
8. Budget and requested amounts use ₹1,000 units in the current interface.

## Complexity

For n eligible applicants and budget capacity B in ₹1,000 units:

- 0/1 knapsack DP: O(nB) time and O(nB) memory.
- Branch-and-bound: worst-case O(2^n), with pruning based on a fractional upper bound.

## Verification

The automated tests cover normal allocation, ineligible exclusion, zero budget, invalid budget units, invalid request units, and agreement between DP and branch-and-bound.
