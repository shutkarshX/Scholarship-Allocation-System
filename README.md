# Intelligent Scholarship Allocation System

A Data Structures and Algorithms-II PBL project for transparent, explainable, and budget-constrained scholarship allocation.

## Project Goal

The system evaluates scholarship applicants using academic merit, financial need, and attendance; ranks eligible applicants; and allocates a limited scholarship fund using algorithmic techniques.

## Current Development Status

**Phase 1 — Foundation**

The repository now contains the initial system specification, scholarship policy baseline, core eligibility/scoring services, hash-based lookup, sample data, a minimal Flask dashboard, and initial unit tests.

The existing DSA algorithm modules are being validated and integrated rather than treated as automatically complete.

## Core Flow

Applicant Management
        ↓
Eligibility Check
        ↓
Priority Score
        ↓
Applicant Ranking
        ↓
Budget Allocation
        ↓
Results / Explanation

## DSA Direction

Planned/being validated:
- Hash-table based applicant lookup
- Merge Sort for complete ranking
- Priority Queue / Max Heap
- Greedy allocation baseline
- Dynamic Programming / 0/1 Knapsack-style allocation
- Time and space complexity analysis

These techniques are selected because they map to actual system operations. Final implementation decisions will be based on testing and the finalized system design.

## Baseline Scoring

- Academic Merit: 40%
- Financial Need: 40%
- Attendance: 20%

See docs/SYSTEM_SPEC.md for the current policy and formulas.

## Project Structure

backend/
├── algorithms/
├── services/
├── tests/
└── app.py

data/
└── sample_students.json

frontend/
├── static/
└── templates/

docs/
├── SYSTEM_SPEC.md
└── DEVELOPMENT_LOG.md

## Running the web app

Create/activate a Python environment, install the requirements, then run:

python backend/app.py

The development server will expose the dashboard locally.

## Academic Context

Course: Data Structures and Algorithm-II
Course Code: CCSE0301
Project: Intelligent Scholarship Allocation System
SDG: SDG 4 – Quality Education
Assignment: Individual