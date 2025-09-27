# backend/services/gap_analyzer.py
from .retriever import load_job_description

def analyze_gap(role: str, user_skills: list):
    """
    Compare user skills with required role skills.
    Returns the list of missing skills.
    """

    # Load job description for the given role
    required = load_job_description(role)

    if not required:
        return []  # no role found in jds.json

    # Flatten required skills dict into a single list
    required_skills = []
    for category, skills in required.items():
        required_skills.extend(skills)

    # Normalize to lowercase for comparison
    user_skills_lower = [s.lower() for s in user_skills]
    required_skills_lower = [s.lower() for s in required_skills]

    # Compute missing skills
    missing = [
        skill for skill in required_skills
        if skill.lower() not in user_skills_lower
    ]

    return missing