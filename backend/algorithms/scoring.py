"""Priority score calculation for scholarship applicants."""


def calculate_need_score(family_income: float) -> float:
    """Convert annual family income into a transparent 0-100 need score."""
    if family_income <= 100_000:
        return 100.0
    if family_income <= 200_000:
        return 90.0
    if family_income <= 300_000:
        return 80.0
    if family_income <= 500_000:
        return 65.0
    if family_income <= 800_000:
        return 40.0
    return 20.0


def calculate_merit_score(cgpa: float) -> float:
    """Convert CGPA on a 10-point scale into a 0-100 merit score."""
    if not 0 <= cgpa <= 10:
        raise ValueError("CGPA must be between 0 and 10")
    return cgpa * 10


def calculate_attendance_score(attendance: float) -> float:
    """Use attendance percentage directly as the attendance score."""
    if not 0 <= attendance <= 100:
        raise ValueError("Attendance must be between 0 and 100")
    return attendance


def calculate_priority_score(
    cgpa: float,
    family_income: float,
    attendance: float,
    merit_weight: float = 0.50,
    need_weight: float = 0.35,
    attendance_weight: float = 0.15,
) -> float:
    """Calculate the weighted scholarship priority score."""
    if abs(merit_weight + need_weight + attendance_weight - 1.0) > 1e-9:
        raise ValueError("Score weights must sum to 1.0")

    merit = calculate_merit_score(cgpa)
    need = calculate_need_score(family_income)
    attendance_score = calculate_attendance_score(attendance)

    return round(
        merit * merit_weight
        + need * need_weight
        + attendance_score * attendance_weight,
        2,
    )
