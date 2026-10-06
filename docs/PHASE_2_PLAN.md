# Phase 2 Plan — Scholarship Allocation System

## Status

Phase 1 is locked at commit `33c8b3ee973975a0be9ba17cb445b72c0b734a47`.

This document is a planning checkpoint for Phase 2. It does not claim that Phase 2 work has already been completed.

## Phase 2 objective

Extend the Phase 1 applicant-evaluation system with a genuine DSA-II ranking mechanism.

The current Phase 1 flow is:

```
Applicant Data
    ↓
Eligibility Evaluation
    ↓
Priority Score
    ↓
Hash-based Lookup
    ↓
Dashboard / API
```

The Phase 2 target is:

```
Eligible Applicants
    ↓
Priority Scores
    ↓
Heap / Priority Queue
    ↓
Ranked Applicants
    ↓
Dashboard / API
```

The ranking mechanism is the main Phase 2 development target because it directly connects the existing priority score to Unit 1 concepts from DSA-II.

## Why this concept

The DSA-II Unit 1 syllabus includes heaps and priority queues.

The project already calculates a priority score for each eligible applicant. A priority queue provides a natural way to repeatedly obtain the highest-priority eligible applicant without treating sorting as the project's only DSA contribution.

The implementation should therefore use a heap-backed priority queue for applicant ranking.

We will not add dynamic programming, graph algorithms, branch-and-bound, or advanced trees in Phase 2 merely because they may be useful later. Those concepts remain future options and will be mapped to later phases only when the official phase requirements and project need justify them.

## Phase 2 scope

### In scope

1. Define ranking behavior for eligible applicants.
2. Build a heap / priority-queue based ranking component.
3. Feed the existing Phase 1 priority scores into the ranking structure.
4. Produce an ordered list of eligible applicants.
5. Handle equal priority scores deterministically.
6. Exclude ineligible applicants from the ranking.
7. Expose the ranked result through the existing application/API where appropriate.
8. Add automated tests for the ranking behavior.
9. Run the application and manually verify the ranked output.
10. Record genuine evidence and development notes after the implementation is tested.

### Out of scope for Phase 2

- Scholarship budget allocation.
- 0/1 Knapsack.
- Dynamic programming allocation optimization.
- Graph-based allocation.
- Branch-and-bound.
- Advanced trees such as red-black/B-tree/B+ tree.
- Fabricated institutional scholarship rules.
- Replacing the existing eligibility policy without evidence.
- Claiming research, results, screenshots, or testing before they actually happen.

## Proposed ranking behavior

Only applicants who pass the existing Phase 1 eligibility policy enter the ranking structure.

Each eligible applicant is associated with the priority score already calculated in Phase 1.

The heap should return the highest-priority applicant first.

For equal priority scores, a deterministic secondary rule should be selected and documented before implementation so repeated runs produce a predictable order.

The ranking component should not change the existing eligibility decision or priority-score formula.

## Expected component boundary

A new ranking module should have a narrow responsibility:

```
Applicant records
      ↓
filter eligible
      ↓
priority score
      ↓
priority queue / heap
      ↓
ranked records
```

The existing modules remain responsible for:

- eligibility policy → `backend/services/eligibility.py`
- priority calculation → `backend/algorithms/scoring.py`
- applicant lookup → `backend/algorithms/hashing.py`
- applicant persistence → `backend/services/applicant_store.py`

This keeps Phase 2 additive instead of rewriting the Phase 1 foundation.

## Testing plan

Before considering Phase 2 complete, tests should cover at least:

1. Highest-priority eligible applicant is returned first.
2. Multiple applicants are returned in correct priority order.
3. Ineligible applicants do not appear in the ranking.
4. Equal scores follow the documented deterministic tie-break rule.
5. Empty eligible input is handled correctly.
6. A single eligible applicant is handled correctly.
7. Existing Phase 1 tests continue to pass.
8. The application/API exposes the expected ranked result.

The actual test count and results will be recorded only after the tests are executed.

## Evidence plan

Evidence will be captured only after real implementation and verification.

Potential evidence:

- automated test output;
- dashboard showing ranked eligible applicants;
- API response showing ranked data, if exposed;
- relevant code/module view;
- development log entry.

No screenshot or result will be described as completed until it has actually been produced.

## Review 2 mapping

The official Review 2 requirements will be addressed from actual work:

| Review 2 requirement | Phase 2 treatment |
|---|---|
| Previous Review Feedback | Record only actual faculty feedback; if none is available, do not invent it |
| Action Taken | Document actual response to available feedback |
| Research / Data Collection Progress | Record research actually completed for heap/priority-queue ranking |
| Unit/Module Concepts Applied | Heap / priority queue from DSA-II Unit 1 |
| Methodology / Approach | Eligibility → score → priority queue → ranking |
| Work Completed During Month 2 | Record only completed Phase 2 work |
| Analysis / Development / Implementation | Explain the ranking implementation |
| Results / Interim Outcomes | Record actual test/application results |
| Evidence / Supporting Material | Attach genuine test/UI/API/code evidence |
| Challenges & Corrective Actions | Record real implementation issues and fixes |
| Individual / Team Contribution | Individual implementation by Utkarsh Sharma |
| Overall Progress | Calculate after actual Phase 2 work, not in advance |
| Plan for Final Review | Decide from the completed Phase 2 state |

## Phase 2 completion gate

Phase 2 will be considered complete only when:

- the heap/priority-queue ranking is implemented;
- the implementation is integrated without breaking Phase 1;
- automated tests pass;
- the application is manually verified;
- actual evidence is available;
- the development log is updated;
- the final Phase 2 checkpoint is committed.

Only then should we prepare the material needed for Report 2.

## Next action

Implement the ranking component only after confirming the exact heap/priority-queue behavior and tie-breaking rule. No allocation optimization should be started as part of this phase.
