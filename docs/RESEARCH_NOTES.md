# Research Notes — Scholarship Allocation System

> Current-phase research only. These notes record sources reviewed for the project; they do not claim that future algorithms have already been implemented.

## 1. Scholarship Allocation as a Decision-Support Problem

A 1987 study describes a scholarship allocation decision-support system that combined applicant/data handling with an allocation module and allowed administrators to examine alternative grant combinations. The system was evaluated using actual scholarship data and compared with manual allocation.

**Project relevance:** This supports treating the project as a decision-support system for scholarship administrators rather than only a student-record CRUD application.

## 2. Dynamic Programming and Scholarship Assignment

Huang et al. (2018) studied scholarship assignment as an optimization problem under practical constraints and an equity requirement. Their approach used dynamic programming and a sequence of 0/1 knapsack subproblems to derive feasible scholarship assignment schemes.

**Project relevance:** The scholarship-budget allocation problem has a strong natural connection to the 0/1 knapsack topic in the DSA-II syllabus. This supports the planned future mapping of:

- requested scholarship amount -> allocation cost
- applicant priority score -> allocation value
- available scholarship budget -> capacity

This is a future design direction, not current implementation.

## 3. Recent Work on Budget-Constrained Scholarship Assignment

A 2025 study on a Chilean scholarship case considered scholarship assignment under limited budgets and uncertainty about renewals. It used an approximate dynamic-programming/Markov-decision-process approach and evaluated alternative assignment policies.

**Project relevance:** Real scholarship allocation can involve constraints beyond a simple ranking. For the current project, this reinforces the need to keep policy assumptions explicit and avoid claiming that the simplified project model represents every real institutional scholarship process.

## 4. Current Scope Boundary

The research supports the overall problem direction, but it does **not** determine the project's institutional eligibility thresholds, score weights, or final allocation policy.

The current project-defined baseline remains:

- CGPA >= 6.0
- Attendance >= 75%
- Annual family income <= Rs. 5,00,000
- Academic merit: 40%
- Financial need: 40%
- Attendance: 20%

These are project assumptions and must not be presented as official institutional scholarship rules.

## References

1. Clark et al. (1987), *A microcomputer-based decision support system for scholarship allocation*, Journal of Microcomputer Applications, 10(3), 199–210. DOI: 10.1016/0745-7138(87)90013-3.
2. Huang, D., Gu, Y., Wang, H., Liu, Z., & Chen, J. (2018), *An Incentive Dynamic Programming Method for the Optimization of Scholarship Assignment*, Discrete Dynamics in Nature and Society, 2018, Article 5206131. DOI: 10.1155/2018/5206131.
3. Redondo, S., Cataldo, A., Marquinez, J. T., Rey, P. A., & Sauré, A. (2025), *Improving scholarship assignment using approximate dynamic programming: A Chilean case study*, Socio-Economic Planning Sciences, 102, 102296. DOI: 10.1016/j.seps.2025.102296.
