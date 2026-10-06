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

Only fields with a current purpose should remain.

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

Academic score: `(CGPA / 10) × 100`

Need score: `((income_limit - family_income) / income_limit) × 100`, clamped to 0–100.

Attendance score is the attendance percentage.

Final score: `academic × 0.40 + need × 0.40 + attendance × 0.20`

## 6. Current DSA Work

The repository contains DSA implementations being validated against actual requirements:

- Hash table for applicant lookup
- Merge Sort for applicant ordering
- Max Heap for priority retrieval
- Greedy allocation
- Dynamic programming allocation

A module stays only if testing demonstrates a real purpose. No algorithm is retained simply to increase the DSA count.

## 7. Current Technical Stack

- Python
- Flask
- HTML/CSS
- JSON sample data

No database or additional framework is being introduced at this stage.

## 8. Phase 1 Definition

Phase 1 is concerned only with establishing and validating the foundation:

1. Applicant data and validation
2. Eligibility evaluation
3. Priority scoring
4. Hash-based lookup
5. Minimal web interface
6. Core tests
7. Controlled sample data
8. Genuine development evidence

When these are working and verified, the next phase can be designed from the actual results. Future-phase modules are intentionally not specified or implemented here.
