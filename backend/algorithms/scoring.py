"""Priority score calculation for scholarship applicants."""


def calculate_need_score(
    family_income: float,
    income_limit: float = 500_000,
) -> float:
    """Convert income into a transparent 0-100 financial-need score."""
    if income_limit <= 0:
        raise ValueError("Income limit must be greater than 0")
    if family_income < 0:
        raise ValueError("Family income cannot be negative")

    score = ((income_limit - family_income) / income_limit) * 100
    return round(max(0.0, min(100.0, score)), 2)


def calculate_merit_score(cgpa: float) -> float:
    """Convert CGPA on a 10-point scale into a 0-100 merit score."""
    if not 0 <= cgpa <= 10:
        raise ValueError("CGPA must be between 0 and 10")
    return round(cgpa * 10, 2)


def calculate_attendance_score(attendance: float) -> float:
    """Use attendance percentage directly as the attendance score."""
    if not 0 <= attendance <= 100:
        raise ValueError("Attendance must be between 0 and 100")
    return round(attendance, 2)


def calculate_priority_score(
    cgpa: float,
    family_income: float,
    attendance: float,
    merit_weight: float = 0.40,
    need_weight: float = 0.40,
    attendance_weight: float = 0.20,
    income_limit: float = 500_000,
) -> float:
    """Calculate the weighted scholarship priority score."""
    if abs(merit_weight + need_weight + attendance_weight - 1.0) > 1e-9:
        raise ValueError("Score weights must sum to 1.0")

    merit = calculate_merit_score(cgpa)
    need = calculate_need_score(family_income, income_limit)
    attendance_score = calculate_attendance_score(attendance)

    return round(
        merit * merit_weight
        + need * need_weight
        + attendance_score * attendance_weight,
        2,
    )


def calculate_score_breakdown(
    cgpa: float,
    family_income: float,
    attendance: float,
    income_limit: float = 500_000,
) -> dict:
    """Return component scores and weighted contributions."""
    merit = calculate_merit_score(cgpa)
    need = calculate_need_score(family_income, income_limit)
    attendance_score = calculate_attendance_score(attendance)

    return {
        "academic_score": merit,
        "need_score": need,
        "attendance_score": attendance_score,
        "academic_weighted": round(merit * 0.40, 2),
        "need_weighted": round(need * 0.40, 2),
        "attendance_weighted": round(attendance_score * 0.20, 2),
        "priority_score": calculate_priority_score(
            cgpa,
            family_income,
            attendance,
            income_limit=income_limit,
        ),
    }
