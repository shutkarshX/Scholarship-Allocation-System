# Phase 1 — Intelligent Scholarship Allocation System

## Overview

Phase 1 established the working foundation of the Intelligent Scholarship Allocation System for the DSA-II PBL.

The goal of this phase was not to build the complete scholarship allocation system. It was to build and verify the first layer needed for later stages:

Applicant Data → Eligibility Evaluation → Priority Scoring → Applicant Lookup

Future ranking, budget allocation, optimization, and other advanced modules were intentionally not implemented in Phase 1.

---

## 1. Problem We Are Solving

Scholarship applications contain multiple factors such as:

- Academic performance
- Attendance
- Family income
- Requested scholarship amount
- Category
- Number of dependents
- Previous scholarship status

Evaluating these applicants manually can make it difficult to apply the same eligibility rules consistently and compare applicants using a transparent scoring method.

The project therefore starts with a decision-support foundation that can:

1. Store applicant information.
2. Check whether an applicant satisfies the defined eligibility policy.
3. Calculate a priority score for eligible applicants.
4. Find an applicant efficiently using their roll number.

This is the foundation for the larger scholarship-allocation system planned for later phases.

---

# 2. What We Implemented

## 2.1 Applicant Data

A controlled sample dataset was created for development and testing.

Each applicant contains information such as:

- Roll number
- Name
- Course / branch
- Year
- CGPA
- Attendance
- Annual family income
- Requested scholarship amount
- Category
- Number of dependents
- Previous scholarship status

### Why?

The system needs structured applicant data before eligibility, scoring, or later allocation algorithms can operate.

### How?

Applicant records are represented as Python dictionaries and stored in JSON files.

The controlled development dataset is:

data/sample_students.json

Manual applicant entries are kept separately in:

data/applicants.json

The manual-entry store starts empty and is populated only when a user adds an applicant through the application.

---

# 3. Eligibility Evaluation

## What

The system evaluates whether an applicant satisfies the current scholarship eligibility policy.

The current policy is:

| Rule | Requirement |
|---|---:|
| Minimum CGPA | 6.0 |
| Minimum attendance | 75% |
| Maximum annual family income | ₹500,000 |
| Requested amount | Must be greater than 0 |

An applicant must satisfy the required conditions to be marked Eligible.

If a condition fails, the system returns the corresponding reason.

## Why?

Eligibility should be determined consistently instead of being manually checked for every applicant.

Keeping this logic in a separate service also makes the policy easier to test and change later.

## How?

Eligibility is implemented in:

backend/services/eligibility.py

The service:

1. Validates required applicant fields.
2. Validates numeric values.
3. Checks CGPA.
4. Checks attendance.
5. Checks family income.
6. Checks requested scholarship amount.
7. Returns eligibility status and reasons.

The policy thresholds are kept together in a default policy configuration rather than being scattered throughout the application.

---

# 4. Priority Scoring

## What

Eligible applicants receive a priority score based on three measurable factors:

- Merit
- Financial need
- Attendance

The weights are:

| Factor | Weight |
|---|---:|
| Merit | 40% |
| Financial need | 40% |
| Attendance | 20% |

Therefore:

Priority Score = 0.40 × Merit + 0.40 × Need + 0.20 × Attendance

The final score is on a 0–100 scale.

## Why?

Eligibility only answers:

"Does this applicant satisfy the minimum conditions?"

It does not tell us how strongly an eligible applicant should be prioritized.

A weighted score provides an initial transparent way to compare eligible applicants.

The weights were selected as the project's current scoring policy. They are not presented as an externally established institutional scholarship policy.

## How?

Priority scoring is implemented in:

backend/algorithms/scoring.py

### Merit score

CGPA is converted to a percentage-style score:

Merit = (CGPA / 10) × 100

### Need score

Financial need increases as family income decreases relative to the configured income limit.

The calculation is:

Need = ((Income Limit − Family Income) / Income Limit) × 100

The value is clamped to the 0–100 range.

### Attendance score

Attendance percentage is used directly as the attendance score.

### Final score

The three components are multiplied by their weights and added.

The scoring module also returns the individual components and weighted contributions so that the result is explainable rather than being only a single unexplained number.

---

# 5. Hash-Based Applicant Lookup

## What

The system supports finding an applicant using their roll number.

The implementation uses a hash-table structure:

backend/algorithms/hashing.py

The main class is ApplicantHashTable.

It provides operations for:

- Insert
- Get
- Check existence
- Remove
- Count records

## Why?

Roll number is a natural unique identifier for a student.

A hash-table based lookup provides average O(1) lookup time, making it suitable for direct applicant retrieval.

This also gives the project a concrete DSA-II application instead of using only ordinary sequential searching.

## How?

The implementation uses Python's dictionary as the underlying hash table.

Applicants are indexed by their roll number.

For example:

250133154001 → Aarav Sharma

The API exposes the lookup through:

GET /api/applicants/<roll_no>

An existing roll number returns the corresponding applicant.

An unknown roll number returns an HTTP 404 response.

---

# 6. Applicant Storage and Manual Entry

## What

The application includes a web form for adding an applicant.

The form accepts:

- Roll number
- Name
- Course / branch
- Year
- CGPA
- Attendance
- Annual family income
- Requested amount
- Category
- Dependents
- Previous scholarship status

## Why?

The system should not depend entirely on hard-coded sample data.

A manual-entry flow demonstrates that new applicant records can enter the system and pass through the same evaluation process.

## How?

Applicant storage is handled by:

backend/services/applicant_store.py

The service:

1. Receives a new applicant record.
2. Validates the record.
3. Checks for duplicate roll numbers.
4. Stores valid manual entries in the local JSON store.

The Flask application then evaluates the newly added applicant using the existing eligibility and scoring services.

No database was introduced because a database was not necessary for the current phase.

---

# 7. Flask Application and Dashboard

## What

A minimal Flask application connects the backend components to a browser-based interface.

Main application:

backend/app.py

Dashboard:

frontend/templates/dashboard.html

Styling:

frontend/static/style.css

## Why?

The project is intended to be a decision-support system, so the algorithms should be observable through an actual application rather than existing only as isolated Python functions.

## How?

The Flask application:

1. Loads the controlled sample applicants.
2. Loads any manual applicants.
3. Evaluates eligibility.
4. Calculates priority scores.
5. Sends the evaluated records to the dashboard.
6. Provides API endpoints for applicant data and lookup.
7. Accepts new applicant submissions.

The current dashboard displays:

- Total applicants
- Eligible applicants
- Income limit
- Applicant information
- Eligibility status
- Priority score
- Manual applicant-entry form
- JSON API access

---

# 8. API

The application exposes:

## All applicants

GET /api/applicants

Returns the evaluated applicant data.

## Applicant lookup

GET /api/applicants/<roll_no>

Returns one applicant using hash-based roll-number lookup.

For an unknown roll number, the API returns HTTP 404.

---

# 9. Testing

Testing was performed before considering Phase 1 complete.

The final automated test run produced:

11 tests executed

11 tests passed

0 failures

The tests covered:

- Applicant storage
- Duplicate roll-number protection
- Eligibility for valid applicants
- Income threshold behavior
- Low-attendance rejection
- Need-score calculation
- Score-weight validation
- Hash-based lookup
- API lookup for an existing applicant
- API 404 behavior for an unknown applicant

This gave us automated verification of the core Phase 1 logic.

---

# 10. Browser Verification

After the automated tests passed, the Flask application was run locally and checked through the browser.

The dashboard was verified to:

- Load successfully.
- Display the controlled applicants.
- Show eligible and ineligible states.
- Display priority scores for eligible applicants.
- Accept a manual applicant.
- Display the newly added test applicant correctly.

A temporary applicant named Phase One Test with roll number TEST1001 was used during browser testing.

That record was a test record only and was not retained in the repository dataset.

The repository's data/applicants.json remains an empty manual-entry store.

This keeps the manual-entry store clean.

---

# 11. DSA Concepts Applied in Phase 1

The main DSA-related concept actually implemented in this phase is hash-based lookup.

The project also establishes the data and scoring foundation required for later DSA-II applications.

At this stage, we intentionally did not implement:

- Heap-based ranking
- Priority queues for scholarship ranking
- Graph algorithms
- Dynamic programming allocation
- 0/1 knapsack allocation
- Backtracking
- Branch and bound
- Advanced trees

These remain future work and will only be implemented when the corresponding project phase requires and justifies them.

---

# 12. Why We Did Not Build Everything at Once

The project is being developed phase-by-phase.

Implementing future algorithms before their phase would create two problems:

1. We could not honestly claim that the work belonged to the current review period.
2. We would have implementation without corresponding requirements, testing, and evidence.

Therefore, Phase 1 was kept focused on establishing a verified foundation.

The development principle is:

Requirement → Implementation → Testing → Evidence → Next Phase

---

# 13. Phase 1 File Structure

The important Phase 1 components are:

Scholarship-Allocation-System/
│
├── backend/
│   ├── algorithms/
│   │   ├── hashing.py
│   │   └── scoring.py
│   │
│   ├── services/
│   │   ├── applicant_store.py
│   │   └── eligibility.py
│   │
│   ├── tests/
│   │   ├── test_core.py
│   │   └── test_hash_lookup_api.py
│   │
│   └── app.py
│
├── data/
│   ├── applicants.json
│   └── sample_students.json
│
├── docs/
│   ├── DEVELOPMENT_LOG.md
│   ├── RESEARCH_NOTES.md
│   └── SYSTEM_SPEC.md
│
└── frontend/
    ├── templates/
    │   └── dashboard.html
    └── static/
        └── style.css

---

# 14. Phase 1 Result

At the end of Phase 1, the project has a working and tested foundation:

Applicant Data
      ↓
Validation
      ↓
Eligibility Evaluation
      ↓
Priority Scoring
      ↓
Applicant Lookup
      ↓
Browser Dashboard / API

The system can now accept applicant information, evaluate eligibility, calculate an explainable priority score, and retrieve applicants by roll number.

The automated test suite passes 11/11 tests, and the application has been manually verified through the browser.

---

# 15. Phase 1 Boundary

Phase 1 is considered complete at this point.

The next phase should not be started by simply adding more features to this implementation.

Before Phase 2 development begins, its requirements should be reviewed and mapped to:

- the DSA-II syllabus,
- the existing Phase 1 system,
- the official Review 2 requirements,
- and the evidence that will need to be produced.

Only then should the next implementation be selected.
