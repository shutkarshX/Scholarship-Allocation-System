"""Minimal Flask application for the scholarship system."""

import json
from pathlib import Path

from flask import Flask, jsonify, render_template

from algorithms.hashing import ApplicantHashTable
from algorithms.scoring import calculate_score_breakdown
from services.eligibility import DEFAULT_POLICY, evaluate_eligibility

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "sample_students.json"

app = Flask(
    __name__,
    template_folder=str(ROOT / "frontend" / "templates"),
    static_folder=str(ROOT / "frontend" / "static"),
)


def load_applicants() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


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
    return render_template(
        "dashboard.html",
        applicants=applicants,
        eligible_count=sum(a["eligible"] for a in applicants),
        policy=DEFAULT_POLICY,
    )


@app.get("/api/applicants")
def applicants_api():
    return jsonify(evaluate_applicants())


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
