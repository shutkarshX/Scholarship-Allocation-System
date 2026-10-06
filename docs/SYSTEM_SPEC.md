# System Specification — Intelligent Scholarship Allocation System

> Current implementation specification only. Future features are intentionally not included until they are needed.

## 1. Objective

Build a decision-support system that evaluates scholarship applicants using defined eligibility rules and a transparent priority score.

The project is primarily a DSA-II implementation. The web interface exists to make the current system usable and demonstrable.

## 2. Current User

Scholarship Administrator / Scholarship Committee.

No student login or account system is part of the current phase.

## 3. Current Applicant Record

Fields currently used by the application:

- Roll Number
- Name
- Course / Branch
- Year
- CGPA
- Attendance %
- Annual Family Income
- Requested Amount
- Category
- Dependents
- Previous Scholarship

These fields support the current applicant-entry and evaluation flow.

## 4. Current Eligibility Policy

An applicant is eligible when:

- CGPA >= 6.0
- Attendance >= 75%
- Annual family income <= ₹5,00,000
- Required fields are valid/present
- Requested scholarship amount > ₹0

These are project-defined baseline rules, not claims about an institution's official scholarship policy.

The system returns reasons for ineligibility.

## 5. Current Priority Score

All components are normalized to 0–100.

- Academic Merit: 40%
- Financial Need: 40%
- Attendance: 20%

Academic score: (CGPA / 10) × 100

Need score: ((income_limit - family_income) / income_limit) × 100, clamped to 0–100.

Attendance score is the attendance percentage.

Final score: academic × 0.40 + need × 0.40 + attendance × 0.20

## 6. Current DSA Work

The current DSA component is hash-based applicant lookup.

- Applicant records are stored in a hash-table abstraction.
- Roll number is used as the lookup key.
- Lookup is expected to be O(1) average time.
- The implementation is validated through automated tests and the web API.

Other algorithms are intentionally not stored or implemented until a later phase requires them.

## 7. Current Applicant Management

Applicants can be entered manually through the web interface.

- The form collects the current applicant fields.
- Input is validated before storage.
- Roll numbers must be unique.
- Records are stored in the local controlled JSON dataset.
- The same eligibility and scoring logic is applied after an applicant is added.

This is local development storage; no database is introduced at this stage.

## 8. Current Technical Stack

- Python
- Flask
- HTML/CSS
- JSON sample data

No database or additional framework is being introduced at this stage.

## 9. Phase 1 Definition

Phase 1 is concerned only with establishing and validating the foundation:

1. Applicant data and validation
2. Manual applicant entry
3. Eligibility evaluation
4. Priority scoring
5. Hash-based lookup
6. Minimal web interface
7. Core tests
8. Controlled sample data
9. Genuine development evidence

When these are working and verified, the next phase can be designed from the actual results. Future-phase modules are intentionally not specified or implemented here.
