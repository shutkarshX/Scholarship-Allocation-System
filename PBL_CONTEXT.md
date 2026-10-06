# PBL Context — Intelligent Scholarship Allocation System

## Project Identity
- Repository: shutkarshX/Scholarship-Allocation-System
- Project: Intelligent Scholarship Allocation System
- Course: Data Structures and Algorithm-II (CCSE0301)
- Assignment: Individual
- Student: Utkarsh Sharma
- Roll No.: 2501331540283
- Domain: Quality Education
- SDG: 4 — Quality Education
- Stack: Python, Flask, HTML/CSS, JSON

## Reporting / Phase Rules
- College PBL reports are phase/review based.
- Report 1 was already submitted and must not be recreated or backdated.
- Report 1 contains claims the user says were not actually completed; do not use those claims as evidence.
- Official Review 2 coverage is Unit 3 and Unit 4.
- Never fabricate faculty feedback, research, implementation, testing, screenshots, results, or progress.
- Future-phase features must not be implemented early merely because they may be useful.
- Use actual repository history, tests, browser verification, and screenshots as evidence.
- Report 2 is drafted from verified work; its DOCX has not been finalized in this checkpoint.

## Completed Development

### Project Phase 1 — Complete
Foundation implemented and verified:
- applicant management/manual entry
- eligibility evaluation
- priority scoring
- hash-based applicant lookup
- Flask dashboard/API
- controlled sample data
- tests
- browser verification

Checkpoint:
- `33c8b3ee973975a0be9ba17cb445b72c0b734a47`
- `checkpoint: mark Phase 1 completed`
- 11/11 tests passed at checkpoint.

### Project Phase 2 — Complete
Heap-based ranking implemented:
- `ScholarshipPriorityQueue` using `heapq`
- eligible applicants only
- existing priority scores reused
- deterministic roll-number tie-break
- ranking API
- dashboard ranking
- ranking tests
- browser/API verification

Checkpoint:
- `8b9b8e641e0cfa65c0718bda08b74ed10b769fdf`

### Review 2 / Unit 3 + Unit 4 — Complete Technical Checkpoint
Implemented:
- exact 0/1 Knapsack Dynamic Programming
- Branch-and-Bound exact solver
- budget-constrained allocation
- deterministic allocation tie-breaking
- dashboard allocation section
- allocation API
- allocation tests and API tests
- GitHub Actions workflow
- frontend API links hidden from user-facing dashboard

Important allocation assumptions:
- only eligible applicants enter allocation
- full requested amount only; no partial awards
- each applicant at most once
- fixed budget per run
- no category quota/institutional reservation rule
- priority score is optimization value
- equal-value tie: lower spending, then deterministic roll-number ordering
- budget/request amounts use ₹1,000 units
These are project assumptions, not official institutional scholarship rules.

Review 2 checkpoint:
- `32e0fd19117d147a022354e05f071c397fae03b7`
- `checkpoint: complete Review 2`

Recent supporting commits include:
- `e09fc9f86b8a301c2ad0baf1c49246df06c36098` — deterministic allocation tie-breaking
- `f1a2e82d5050e1093dbb9137039987b7d6da91b7` — allocation tie-breaking and edge-case tests
- `0bb6f389b48730b58ac97edb4b48924078766613` — hide developer API links from dashboard

## Verified Review 2 Evidence
Local backend test command:
`python -m unittest discover -s tests -v` from `backend`

Latest verified result:
- 36 tests
- 36 passed
- 0 failures

Controlled browser allocation case:
- Budget: ₹100,000
- Awarded: ₹90,000
- Remaining: ₹10,000
- Total priority value: 257.0
- Selected: Ananya Verma (₹25,000), Priya Gupta (₹20,000), Ishita Kapoor (₹45,000)
- DP and Branch-and-Bound selected the same applicants/value.

Evidence screenshots captured by user:
- SS1: allocation result + DP/B&B cross-check
- SS2: complete applicant evaluation/ranking table
Use these as actual evidence; do not claim other screenshots exist.

## Research
`docs/RESEARCH_NOTES.md` records three reviewed scholarship-allocation sources:
1. Clark et al. (1987), scholarship allocation decision-support system.
2. Huang et al. (2018), scholarship assignment using Dynamic Programming and 0/1 knapsack.
3. Redondo et al. (2025), budget-constrained scholarship assignment using approximate Dynamic Programming.
These sources support the decision-support/optimization framing but do not establish institutional eligibility thresholds, score weights, or allocation policy.

## Current Project Pipeline
Applicant Intake
→ Eligibility Evaluation
→ Priority Scoring
→ Heap-Based Ranking
→ Budget-Constrained Allocation
→ DP / Branch-and-Bound
→ Final Allocation

## Current Controlled Eligibility / Scoring Baseline
Project-defined, not official institutional policy:
- CGPA >= 6.0
- Attendance >= 75%
- Annual family income <= ₹5,00,000
- Academic merit 40%
- Financial need 40%
- Attendance 20%

## Current Report 2 Status
Technical implementation and evidence are complete.
Report 2 content has been drafted.
Still do not invent:
- Review 1 faculty feedback
- additional research not actually performed
- broader real-world validation
- performance benchmarks not run
- institutional scholarship rules
- final completion claims beyond verified scope.

A reasonable current project progress figure used in the draft is 70%, but this is a project-management estimate, not a measured institutional metric.

## Next Stage
Move to final-phase planning only after preserving this checkpoint. Do not add Unit 5 or other algorithms just to satisfy the syllabus; add future concepts only if final project requirements genuinely justify them.
