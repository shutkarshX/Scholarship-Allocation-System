# Phase 2 — Heap-Based Applicant Ranking

## Status

Phase 2 is complete.

The Phase 1 checkpoint remains intact. Phase 2 extends the existing eligibility and priority-scoring flow with a heap-based priority queue and applicant ranking.

## Objective

Phase 1 produced an eligibility decision and a priority score for each applicant.

Phase 2 adds the next decision-support step:

```
Eligible Applicants
      ↓
Priority Scores
      ↓
Heap / Priority Queue
      ↓
Ranked Applicants
```

The implementation uses a binary heap through Python's `heapq` module, with negative scores to obtain max-priority behavior from Python's min-heap.

## DSA-II concept applied

The implemented concept is:

- Unit 1 — Heap / Priority Queue

The priority queue is appropriate because the system needs to repeatedly retrieve the applicant with the highest priority score.

The project does not claim that graphs, dynamic programming, branch-and-bound, or advanced trees were applied in Phase 2.

## Implementation

A new module was added:

```
backend/algorithms/ranking.py
```

It contains:

- `ScholarshipPriorityQueue`
- `push()`
- `pop()`
- `peek()`
- `rank_all()`
- `rank_eligible_applicants()`

### Ranking rules

1. Only eligible applicants enter the ranking queue.
2. The existing Phase 1 `priority_score` is used unchanged.
3. Higher priority scores are returned first.
4. Equal scores use roll number as a deterministic tie-breaker.
5. Ranking numbers are assigned from 1 upward.
6. Invalid queue input is rejected rather than silently ranked.

The Phase 1 eligibility rules and priority-score formula were not changed.

## Application integration

The Flask application now:

1. evaluates all applicants using the existing Phase 1 services;
2. sends eligible applicants to the heap-based ranking component;
3. exposes the ranked result to the dashboard;
4. exposes the ranked result through:

```
GET /api/rankings
```

The dashboard now includes an Applicant Ranking section above the detailed Applicant Evaluation table.

## Verification

The complete automated test suite was run locally after pulling the Phase 2 implementation.

Result:

- 21 tests executed
- 21 tests passed
- 0 failures

The suite includes the original Phase 1 tests plus Phase 2 ranking tests covering:

- highest-priority applicant retrieval;
- descending ranking order;
- exclusion of ineligible applicants;
- deterministic tie-breaking;
- empty input;
- single applicant;
- invalid queue insertion;
- missing priority score;
- empty queue behavior;
- ranking API response.

## Browser verification

The Flask application was started locally and the dashboard loaded successfully.

The controlled dataset contained 8 applicants:

- 6 eligible
- 2 ineligible

The displayed ranking was:

| Rank | Applicant | Priority |
|---:|---|---:|
| 1 | Ananya Verma | 88.4 |
| 2 | Ishita Kapoor | 86.8 |
| 3 | Meera Joshi | 82.2 |
| 4 | Priya Gupta | 81.8 |
| 5 | Aarav Sharma | 81.4 |
| 6 | Kabir Mehta | 67.6 |

Rohan Singh and Dev Malhotra were not present in the ranking because they were ineligible under the existing Phase 1 rules.

The browser output therefore confirmed that the ranking layer uses the eligibility result rather than ranking every applicant indiscriminately.

## API verification

The endpoint:

```
/api/rankings
```

was opened in the browser and returned the ranked applicants as JSON.

The response confirmed:

- ranks 1 through 6;
- descending priority scores;
- all returned applicants marked eligible;
- complete applicant information preserved;
- score breakdown preserved;
- the same ranking order as the dashboard.

## UI development

The dashboard visual system was also refined during Phase 2.

The final direction uses:

- deep blue-green application background;
- warm cream workspace surfaces;
- restrained rust accent;
- editorial serif headings;
- compact data tables;
- clear application form hierarchy;
- responsive layout.

The purpose was to make the system feel like a usable scholarship decision-support product rather than a plain white Flask demo.

The UI changes do not alter the eligibility, scoring, ranking, or API logic.

## Complexity

For the heap-based priority queue:

- insertion: average/worst-case `O(log n)`;
- highest-priority removal: `O(log n)`;
- peek: `O(1)`;
- ranking all `n` eligible applicants by repeated heap removal: `O(n log n)`;
- heap storage: `O(n)`.

## Phase 2 boundary

The system can now evaluate and rank applicants, but it does not yet perform final scholarship allocation against a limited budget.

The next allocation stage must be designed separately. Dynamic programming / 0/1 knapsack remains a future implementation decision and has not been added to Phase 2.

## Evidence status

Actual evidence available for this phase:

- local automated test output: 21/21 passed;
- local Flask server output showing successful application requests;
- browser dashboard ranking output;
- browser `/api/rankings` JSON response.

No additional evidence is claimed beyond these verified results.

## Phase 2 result

Phase 2 successfully extends the working system from:

```
Eligibility + Priority Scoring
```

to:

```
Eligibility + Priority Scoring + Heap-Based Ranking
```

This is the verified Phase 2 checkpoint before the next allocation-focused development stage.
