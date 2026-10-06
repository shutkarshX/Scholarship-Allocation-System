"""Scholarship eligibility rules."""


DEFAULT_POLICY = {
    "min_cgpa": 6.0,
    "min_attendance": 75.0,
    "max_family_income": 500_000,
}


def validate_applicant(applicant: dict) -> list[str]:
    errors = []

    required = [
        "roll_no",
        "name",
        "course",
        "year",
        "cgpa",
        "attendance",
        "family_income",
        "requested_amount",
    ]

    for field in required:
        if applicant.get(field) in (None, ""):
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    try:
        cgpa = float(applicant["cgpa"])
        attendance = float(applicant["attendance"])
        income = float(applicant["family_income"])
        requested = float(applicant["requested_amount"])
    except (TypeError, ValueError):
        return ["CGPA, attendance, family income, and requested amount must be numeric"]

    if not 0 <= cgpa <= 10:
        errors.append("CGPA must be between 0 and 10")
    if not 0 <= attendance <= 100:
        errors.append("Attendance must be between 0 and 100")
    if income < 0:
        errors.append("Family income cannot be negative")
    if requested <= 0:
        errors.append("Requested scholarship amount must be greater than 0")

    return errors


def evaluate_eligibility(
    applicant: dict,
    policy: dict | None = None,
) -> dict:
    policy = {**DEFAULT_POLICY, **(policy or {})}
    errors = validate_applicant(applicant)

    if errors:
        return {
            "eligible": False,
            "reasons": errors,
        }

    cgpa = float(applicant["cgpa"])
    attendance = float(applicant["attendance"])
    income = float(applicant["family_income"])

    reasons = []

    if cgpa < policy["min_cgpa"]:
        reasons.append(
            f"CGPA {cgpa:g} is below the minimum {policy['min_cgpa']:g}"
        )
    if attendance < policy["min_attendance"]:
        reasons.append(
            f"Attendance {attendance:g}% is below the minimum "
            f"{policy['min_attendance']:g}%"
        )
    if income > policy["max_family_income"]:
        reasons.append(
            f"Family income ₹{income:,.0f} exceeds the maximum "
            f"₹{policy['max_family_income']:,.0f}"
        )

    return {
        "eligible": not reasons,
        "reasons": reasons or ["Applicant satisfies all baseline eligibility rules"],
    }
