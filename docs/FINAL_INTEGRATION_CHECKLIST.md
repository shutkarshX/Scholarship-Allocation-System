# Final Integration Checklist

This file is a working checklist for the final implementation stage. It deliberately separates completed implementation from evidence that still needs to be captured.

## Existing implemented pipeline

Applicant intake
→ Eligibility evaluation
→ Weighted priority scoring
→ Hash-based applicant lookup
→ Heap-based ranking
→ 0/1 Knapsack allocation using Dynamic Programming
→ Branch-and-Bound cross-check
→ Flask dashboard and API

## Existing verified evidence

- The user ran `python -m unittest discover -s tests -v` locally from `backend`.
- Result: 36 tests passed, 0 failures.
- The user opened the dashboard in a browser.
- The user added a valid applicant through the form and observed the applicant count increase from 8 to 9.
- The dashboard showed a ₹100,000 budget, ₹90,000 awarded, ₹10,000 remaining, and matching DP / Branch-and-Bound selected sets for the preloaded sample case.

These are conversation-confirmed observations. Preserve the actual screenshots separately; this checklist does not claim screenshot files are committed.

## Final validation hardening in progress

A pull request on branch `final-validation-hardening` adds server-side checks for:
- positive integer academic year;
- non-negative integer dependents;
- finite numeric values;
- positive requested scholarship amount in ₹1,000 units;
- regression tests for these cases.

Do not mark this change as merged or verified until its CI run passes and the pull request is merged.

## Final manual evidence still to capture

1. Clean dashboard with the controlled sample dataset.
2. Applicant registration success and updated applicant count.
3. Eligibility evaluation showing both eligible and ineligible examples.
4. Heap ranking in priority order.
5. Budget allocation result with DP / Branch-and-Bound cross-check.
6. Relevant automated test result.

Capture screenshots from the real running application. Do not fabricate, edit values into, or recreate screenshots.

## Data hygiene

- Keep `data/sample_students.json` as the controlled demonstration dataset.
- Keep `data/applicants.json` for user-added records.
- Before final demonstration, inspect and remove only deliberate test records from the local data file after preserving any needed evidence.
- Do not overwrite the sample dataset with the user's test applicant.
- Do not claim persistence across restart until it has been checked.

## Report preparation gate

Prepare the final consolidated report only after:
- the final code state is identified by commit;
- CI and local tests for that state are verified;
- the browser workflow has been demonstrated;
- screenshots have been captured;
- Report I, Report II, topic approval, and the official report format have been reconciled.

The report must distinguish project-defined assumptions from official institutional policy. The CGPA, attendance, income, score weights, and full-request allocation model are project assumptions unless separately supported by an approved source.
