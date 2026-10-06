# Development Log — Intelligent Scholarship Allocation System

> Record only work that actually happened. This file is a history, not a future task list.

## 2026-10-07 — Repository Cleanup Direction

The repository was reviewed using two rules:

1. If a file is not useful to the current project, it should not remain just because it already existed.
2. Do not create future-phase features early. Build the current phase first and create later work when it becomes necessary.

## 2026-10-07 — Phase 1 Applicant Management

The Phase 1 foundation was extended with a manual applicant-entry flow.

Completed work:

- Added a local applicant storage service using the existing JSON dataset.
- Added a web form for entering applicant records.
- Added validation before a new record is stored.
- Added duplicate roll-number protection.
- Connected newly added records to the existing eligibility and priority-score evaluation.
- Added automated tests for applicant storage and duplicate detection.
- Updated the dashboard to expose the manual-entry flow.
- Kept storage local and did not introduce a database.

The controlled sample dataset remains the baseline development dataset. A temporary applicant was used during local browser testing and was not retained in the repository dataset.

## 2026-10-07 — Phase 1 Verification

The complete automated test suite was executed locally after the applicant lookup tests were added.

Result:

- 11 tests executed
- 11 tests passed
- 0 failures

The browser application was also started locally and manually checked.

Verified through the running dashboard:

- Dashboard loads successfully.
- Controlled applicants are displayed and evaluated.
- Eligibility status is calculated for eligible and ineligible cases.
- Priority scores are displayed for eligible applicants.
- Manual applicant entry works.
- A temporary test applicant appeared correctly after submission.
- The current API lookup functionality was covered by the automated tests.

The temporary browser-test applicant was removed from the local test state; the repository's `data/applicants.json` remains an empty manual-entry store.

## Current Repository State

The repository contains the foundation needed for the present development stage:

- applicant sample data
- manual applicant entry
- eligibility service
- scoring service
- hash-based applicant lookup
- minimal Flask application
- minimal dashboard
- core tests
- project documentation

No future-phase ranking, allocation, or optimization modules are being added in advance.

## Project Integrity Rule

Existing scaffold code is not automatically treated as completed project work. It must be tested and verified before it is described as implementation evidence.

Future functionality must not be presented as completed simply because it has been discussed.

## 2026-10-07 — Phase 1 Research and Lookup Verification Coverage

The project research was documented using scholarship-allocation decision-support literature. The reviewed work supports the project's overall decision-support framing and the later connection between budget-constrained scholarship assignment and 0/1 knapsack/dynamic programming. These sources do not determine the project's institutional policy thresholds or score weights.

A separate API-level test file was added for the current hash-based applicant lookup:

- Existing roll number returns the corresponding applicant.
- Unknown roll number returns HTTP 404 with an explicit error.

The API lookup tests are included in the complete 11-test suite described above.

## Phase 1 Checkpoint — Completed

Phase 1 is officially marked complete after implementation, automated testing, and browser verification. This commit is the Phase 1 checkpoint before Phase 2 development begins.


## 2026-10-07 — Phase 2 Heap-Based Ranking

Phase 2 extended the Phase 1 eligibility and priority-scoring pipeline with a heap-based priority queue.

Completed work:

- Added `backend/algorithms/ranking.py`.
- Implemented `ScholarshipPriorityQueue` using Python's `heapq`.
- Ranked only eligible applicants.
- Used the existing Phase 1 priority score without changing its formula.
- Added deterministic roll-number tie-breaking for equal scores.
- Added `GET /api/rankings`.
- Added the Applicant Ranking section to the dashboard.
- Added dedicated ranking tests and ranking API coverage.
- Refined the dashboard visual system into a deep blue-green application shell with warm cream workspace surfaces and a restrained accent palette.

Verification:

- 21 tests executed.
- 21 tests passed.
- 0 failures.
- Browser dashboard successfully displayed 6 eligible applicants in descending priority order.
- `/api/rankings` returned the same verified ranking as JSON.
- The 2 ineligible controlled applicants were excluded from the ranking.

The repository's manual applicant store was cleaned before verification, leaving the controlled 8-applicant dataset as the local baseline.

Phase 2 does not implement scholarship budget allocation or dynamic programming. Those remain future development stages.
