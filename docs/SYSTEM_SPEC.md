# System Specification — Intelligent Scholarship Allocation System

> Design baseline for implementation. This records decisions before coding so implementation and later reports can be traced to a deliberate specification.

## 1. Objective

Build a web-based decision-support system that helps a scholarship committee manage applicants, determine eligibility, calculate a transparent priority score, rank eligible applicants, allocate a limited scholarship budget, and explain results.

The project is primarily a DSA-II implementation. The website is the interface for demonstrating the algorithms.

## 2. Primary user

Scholarship Administrator / Scholarship Committee

Version 1 does not require student login/accounts.

## 3. Applicant record

Required fields:
- Roll Number — unique applicant identifier and hash lookup key
- Name — identification/display
- Course / Branch — applicant information
- Year — applicant information
- CGPA — academic merit
- Attendance % — eligibility + score
- Annual Family Income — financial-need calculation + eligibility
- Requested Amount — allocation cost
- Category — applicant information / future policy extension
- Dependents — financial-context information / future scoring extension
- Previous Scholarship — policy/context information

Only fields with a defined system purpose should remain in the final schema.

## 4. Eligibility policy — initial baseline

An applicant is eligible when all baseline conditions are satisfied:
- CGPA >= 6.0
- Attendance >= 75%
- Annual family income <= ₹5,00,000
- Required application fields are valid/present
- Requested scholarship amount > ₹0

These thresholds are project policy defaults, not claims about a real institution's official scholarship rules. They should be configurable in the application.

The system must show an eligibility reason rather than only a boolean result.

## 5. Priority score

Final baseline weighting:
- Academic Merit: 40%
- Financial Need: 40%
- Attendance: 20%

All components are normalized to 0–100 before weighting.

Academic score = (CGPA / 10) × 100

Financial-need score for eligible applicants = ((income_limit - family_income) / income_limit) × 100, clamped to 0–100.

With the default ₹5,00,000 limit:
- ₹0 income → 100
- ₹1,00,000 → 80
- ₹2,50,000 → 50
- ₹5,00,000 → 0

Attendance score = attendance percentage.

Final score = academic_score × 0.40 + need_score × 0.40 + attendance_score × 0.20

Round the displayed score to two decimal places. Retain component scores so the final score is explainable.

## 6. Ranking

Primary ranking key:
1. Higher priority score
2. Higher financial-need score
3. Lower family income
4. Lower requested amount
5. Roll number as deterministic final tie-break

Two DSA demonstrations are planned:
- Merge Sort for complete ordered ranking.
- Max Heap / Priority Queue for repeatedly retrieving the highest-priority applicant.

The project should compare their roles rather than pretending both are necessary for the same operation.

## 7. Applicant lookup

Applicant Roll Number is the unique lookup key.

Use a hash-table-based structure for average O(1) lookup.

## 8. Scholarship allocation

### Baseline policy
- Awards are full-request only in the first version.
- An applicant either receives the requested amount or is not selected.
- Total allocation must never exceed the available budget.
- Only eligible applicants can be selected.

### Objective

Maximize the total priority score of selected applicants while staying within the budget.

This creates a 0/1 knapsack-style model:
- cost = requested scholarship amount
- value = applicant priority score
- capacity = available scholarship budget

### Greedy baseline

Sort eligible applicants by priority_score / requested_amount descending, then select an applicant when the full request fits the remaining budget.

Greedy is a fast heuristic/baseline and is not assumed to be optimal.

### Dynamic programming

Use 0/1 knapsack-style DP to maximize total priority score under the same budget constraint.

Compare selected applicants, budget used, remaining budget, total priority value, and complexity/performance characteristics.

Important limitation: DP is pseudo-polynomial in the integer budget, so the application should use practical budget constraints rather than allowing an arbitrarily huge DP table.

## 9. Fairness / tie-breaking

For equal scores, use deterministic tie-breaking:
1. Higher financial-need score
2. Lower family income
3. Lower requested amount
4. Roll number

The system should state that final scholarship policy remains subject to institutional rules.

## 10. Technology direction

Initial stack:
- Python
- Flask for the web backend
- HTML/CSS/JavaScript for the interface
- JSON/sample data during early development

Do not introduce a database or heavy framework until the project actually needs it.

Reason: keep the system manageable on a low-resource development machine and keep the DSA implementation visible.

## 11. Planned architecture

Browser → Flask routes/API → application/service layer → DSA modules → applicant data/configuration → result returned to UI

Suggested structure:
- backend/app.py
- backend/models/
- backend/services/
- backend/algorithms/
- backend/tests/
- frontend/templates/
- frontend/static/
- data/
- docs/

## 12. Core pages

1. Dashboard
2. Applicants
3. Applicant details
4. Eligibility / Evaluation
5. Ranking
6. Allocation
7. Results / Explanation
8. Algorithms / Complexity
9. Settings / Scholarship Policy

UI should remain simple and functional before visual polish.

## 13. Validation requirements

Test at minimum:
- valid applicant
- invalid CGPA
- invalid attendance
- missing required fields
- income exactly at threshold
- income just above threshold
- attendance exactly at threshold
- CGPA exactly at threshold
- zero/negative requested amount
- duplicate roll number
- empty applicant list
- budget smaller than every request
- budget exactly equal to a request
- budget larger than total requests
- equal priority scores
- greedy and DP producing different selections

## 14. Complexity targets

Final documentation should verify the actual implementation. Initial targets:
- Hash lookup: average O(1)
- Merge Sort: O(n log n)
- Heap insertion: O(log n)
- Heap removal: O(log n)
- Greedy allocation: typically O(n log n) due to sorting
- DP allocation: O(nB) time and O(B) or implementation-appropriate space, where B is the integer budget/capacity representation

## 15. Phase 1 implementation order

1. Lock project structure.
2. Create applicant model/validation.
3. Create configurable scholarship policy.
4. Implement eligibility evaluation.
5. Implement score normalization and weighted scoring.
6. Implement applicant storage and hash lookup.
7. Create unit tests.
8. Add initial Flask API/routes.
9. Create minimal applicant/evaluation UI.
10. Run controlled sample data through the system.
11. Capture genuine evidence.
12. Update the DSA project memo with actual milestones.

## 16. Definition of done for Phase 1

Phase 1 is not complete merely because files exist. It should have:
- a runnable project
- validated applicant records
- working eligibility
- working priority scoring
- working hash lookup
- automated/manual tests
- a minimal usable web interface
- sample data
- recorded evidence
- no unverified completion claims in documentation