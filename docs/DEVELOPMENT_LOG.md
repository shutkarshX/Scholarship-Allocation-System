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

The existing sample dataset remains the controlled development dataset. Manual entries are appended to that dataset during local testing.

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

The tests provide verification coverage for the current DSA lookup component. Actual local execution of the complete updated test suite and browser-based evidence still has to be performed in the developer environment before those results are recorded as completed evidence.

