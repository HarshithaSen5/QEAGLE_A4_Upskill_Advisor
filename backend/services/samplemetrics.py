# metrics_evaluator.py

from collections import Counter

def top_k_skill_coverage(jd_skills, suggested_skills, k=5):
    """
    % of JD skills covered in top-k suggested skills.
    """
    jd_set = set(jd_skills)
    top_k = suggested_skills[:k]
    covered = jd_set.intersection(top_k)
    return len(covered) / len(jd_set) * 100 if jd_set else 0


def path_diversity(suggested_courses):
    """
    Measures redundancy in skills across the path.
    Higher diversity = less repetition.
    """
    all_skills = [skill for course in suggested_courses for skill in course]
    counts = Counter(all_skills)
    unique = len(counts)
    total = len(all_skills)
    return unique / total if total else 0


def manual_rubric(relevance, feasibility, clarity):
    """
    Manual evaluation rubric (1–5 scale each).
    Returns average score.
    """
    return (relevance + feasibility + clarity) / 3


# ----------------------------
# Example for your specific roles
# ----------------------------

# JD definitions (role -> required skills)
jd_data = {
    "SDET": ["QA"],
    "GenAI QA": ["Manual QA"]
}

# Mock suggested learning paths (role -> list of courses -> list of skills)
suggested_paths = {
    "SDET": [
        ["QA Fundamentals", "Automation Basics"],
        ["API Testing", "QA"]
    ],
    "GenAI QA": [
        ["Manual QA", "AI Basics"],
        ["Prompt Testing", "Manual QA"]
    ]
}

if __name__ == "__main__":
    for role, jd_skills in jd_data.items():
        suggested_courses = suggested_paths[role]
        suggested_skills = [s for c in suggested_courses for s in c]

        coverage = top_k_skill_coverage(jd_skills, suggested_skills, k=5)
        diversity = path_diversity(suggested_courses)
        rubric = manual_rubric(4, 5, 4)  # Example manual ratings

        print(f"\nRole: {role}")
        print(f"Top-k Skill Coverage: {coverage:.2f}%")
        print(f"Path Diversity: {diversity:.2f}")
        print(f"Manual Rubric Score: {rubric:.2f}/5")
