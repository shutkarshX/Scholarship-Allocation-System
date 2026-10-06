"""Minimal Flask application for the scholarship system."""

import json
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

from algorithms.hashing import ApplicantHashTable
from algorithms.ranking import rank_eligible_applicants
from algorithms.scoring import calculate_score_breakdown
from services.applicant_store import ApplicantStore
from services.eligibility import DEFAULT_POLICY, evaluate_eligibility, validate_applicant

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DATA_FILE = ROOT / "data" / "sample_students.json"
APPLICANT_DATA_FILE = ROOT / "data" / "applicants.json"
STORE = ApplicantStore(APPLICANT_DATA_FILE)

app = Flask(
    __name__,
    template_folder=str(ROOT / "frontend" / "templates"),
    static_folder=str(ROOT / "frontend" / "static"),
)


def load_applicants() -> list[dict]:
    sample_applicants = json.loads(
        SAMPLE_DATA_FILE.read_text(encoding="utf-8")
    )
    return sample_applicants + STORE.load()


def evaluate_applicants() -> list[dict]:
    applicants = load_applicants()

    for applicant in applicants:
        eligibility = evaluate_eligibility(applicant, DEFAULT_POLICY)
        applicant["eligible"] = eligibility["eligible"]
        applicant["eligibility_reasons"] = eligibility["reasons"]

        if applicant["eligible"]:
            applicant["score_breakdown"] = calculate_score_breakdown(
                applicant["cgpa"],
                applicant["family_income"],
                applicant["attendance"],
                DEFAULT_POLICY["max_family_income"],
            )
            applicant["priority_score"] = applicant["score_breakdown"]["priority_score"]
            applicant["need_score"] = applicant["score_breakdown"]["need_score"]
        else:
            applicant["score_breakdown"] = None
            applicant["priority_score"] = 0
            applicant["need_score"] = 0

    return applicants


@app.get("/")
def dashboard():
    applicants = evaluate_applicants()
    ranked_applicants = rank_eligible_applicants(applicants)
    return render_template(
        "dashboard.html",
        applicants=applicants,
        ranked_applicants=ranked_applicants,
        eligible_count=sum(a["eligible"] for a in applicants),
        policy=DEFAULT_POLICY,
    )


@app.post("/applicants")
def add_applicant():
    applicant = {
        "roll_no": request.form.get("roll_no", "").strip(),
        "name": request.form.get("name", "").strip(),
        "course": request.form.get("course", "").strip(),
        "year": request.form.get("year", "").strip(),
        "cgpa": request.form.get("cgpa", "").strip(),
        "attendance": request.form.get("attendance", "").strip(),
        "family_income": request.form.get("family_income", "").strip(),
        "requested_amount": request.form.get("requested_amount", "").strip(),
        "category": request.form.get("category", "General").strip(),
        "dependents": request.form.get("dependents", "").strip(),
        "previous_scholarship": request.form.get("previous_scholarship") == "true",
    }

    errors = validate_applicant(applicant)

    try:
        applicant["year"] = int(applicant["year"])
        applicant["cgpa"] = float(applicant["cgpa"])
        applicant["attendance"] = float(applicant["attendance"])
        applicant["family_income"] = float(applicant["family_income"])
        applicant["requested_amount"] = float(applicant["requested_amount"])
        applicant["dependents"] = int(applicant["dependents"])
    except (TypeError, ValueError):
        errors.append("Year and dependents must be integers")

    if any(str(existing["roll_no"]) == applicant["roll_no"] for existing in load_applicants()):
        errors.append("An applicant with this roll number already exists")

    if errors:
        current_applicants = evaluate_applicants()
        return render_template(
            "dashboard.html",
            applicants=current_applicants,
            ranked_applicants=rank_eligible_applicants(current_applicants),
            eligible_count=sum(a["eligible"] for a in current_applicants),
            policy=DEFAULT_POLICY,
            form_error="; ".join(errors),
            form_data=applicant,
        ), 400

    try:
        STORE.add(applicant)
    except ValueError as exc:
        current_applicants = evaluate_applicants()
        return render_template(
            "dashboard.html",
            applicants=current_applicants,
            eligible_count=sum(a["eligible"] for a in current_applicants),
            policy=DEFAULT_POLICY,
            form_error=str(exc),
            form_data=applicant,
        ), 400

    return redirect(url_for("dashboard"))


@app.get("/api/applicants")
def applicants_api():
    return jsonify(evaluate_applicants())


@app.get("/api/rankings")
def rankings_api():
    return jsonify(rank_eligible_applicants(evaluate_applicants()))


@app.get("/api/applicants/<roll_no>")
def applicant_api(roll_no: str):
    table = ApplicantHashTable()
    for applicant in evaluate_applicants():
        table.insert(applicant)

    applicant = table.get(roll_no)
    if applicant is None:
        return jsonify({"error": "Applicant not found"}), 404

    return jsonify(applicant)


if __name__ == "__main__":
    app.run(debug=True)
