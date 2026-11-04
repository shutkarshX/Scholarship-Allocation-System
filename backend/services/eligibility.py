"""Scholarship eligibility rules and server-side applicant validation."""

import math


DEFAULT_POLICY = {
    "min_cgpa": 6.0,
    "min_attendance": 75.0,
    "max_family_income": 500_000,
}

BUDGET_UNIT = 1000


def validate_applicant(applicant: dict) -> list[str]:
    """Validate applicant fields before storage or eligibility evaluation."""
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
        "dependents",
    ]

    for field in required:
        value = applicant.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    try:
        year_value = float(applicant["year"])
        dependents_value = float(applicant["dependents"])
        cgpa = float(applicant["cgpa"])
        attendance = float(applicant["attendance"])
        income = float(applicant["family_income"])
        requested = float(applicant["requested_amount"])
    except (TypeError, ValueError):
        return ["Year, dependents, CGPA, attendance, family income, and requested amount must be numeric"]

    numeric_values = {
        "Year": year_value,
        "Dependents": dependents_value,
        "CGPA": cgpa,
        "Attendance": attendance,
        "Family income": income,
        "Requested amount": requested,
    }
    for label, value in numeric_values.items():
        if not math.isfinite(value):
            errors.append(f"{label} must be a finite number")

    if errors:
        return errors

    if year_value < 1 or not year_value.is_integer():
        errors.append("Year must be a positive integer")
    if dependents_value < 0 or not dependents_value.is_integer():
        errors.append("Dependents must be a non-negative integer")
    if not 0 <= cgpa <= 10:
        errors.append("CGPA must be between 0 and 10")
    if not 0 <= attendance <= 100:
        errors.append("Attendance must be between 0 and 100")
    if income < 0:
        errors.append("Family income cannot be negative")
    if requested <= 0:
        errors.append("Requested scholarship amount must be greater than 0")
    elif not requested.is_integer() or requested % BUDGET_UNIT != 0:
        errors.append("Requested scholarship amount must be a multiple of ₹1,000")

    if not str(applicant.get("roll_no", "")).strip():
        errors.append("Roll number cannot be empty")
    if not str(applicant.get("name", "")).strip():
        errors.append("Name cannot be empty")
    if not str(applicant.get("course", "")).strip():
        errors.append("Course / branch cannot be empty")

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
