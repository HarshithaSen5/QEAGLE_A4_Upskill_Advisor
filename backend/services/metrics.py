# from collections import Counter

# def evaluate_path(jd_skills, courses, suggested_path, k=None, manual_rubric=None):
#     """
#     Evaluate a suggested learning path based on metrics.
    
#     jd_skills: list of skills required for the JD
#     courses: dict of all available courses (name -> details with "skills")
#     suggested_path: list of course names recommended
#     k: top-k cutoff for coverage (default = all skills)
#     manual_rubric: dict with {"relevance": int, "feasibility": int, "clarity": int}
#     """

#     # -------------------------------
#     # 1. Top-k Skill Coverage
#     # -------------------------------
#     path_skills = set()
#     for course in suggested_path:
#         if course in courses:
#             path_skills.update(courses[course]["skills"])
    
#     if k is None:
#         k = len(jd_skills)
#     covered = len([s for s in jd_skills[:k] if s in path_skills])
#     coverage_pct = round((covered / min(k, len(jd_skills))) * 100, 2)

#     # -------------------------------
#     # 2. Path Diversity
#     # -------------------------------
#     all_skills = []
#     for course in suggested_path:
#         if course in courses:
#             all_skills.extend(courses[course]["skills"])
    
#     skill_counts = Counter(all_skills)
#     unique_skills = len(skill_counts)
#     total_skills = len(all_skills)
#     diversity_score = round(unique_skills / total_skills, 2) if total_skills > 0 else 0

#     # -------------------------------
#     # 3. Manual Rubric (avg score)
#     # -------------------------------
#     rubric_score = None
#     if manual_rubric:
#         rubric_score = round(sum(manual_rubric.values()) / len(manual_rubric), 2)

#     return {
#         "top_k_coverage_%": coverage_pct,
#         "path_diversity": diversity_score,
#         "manual_rubric_avg": rubric_score
#     }


# # -------------------------------
# # 🔹 Example usage
# # -------------------------------
# jd_skills = ["manual testing", "test cases", "bug tracking", "api testing", "selenium"]
# courses = {
#     "manual testing foundations": {"skills": ["manual testing", "test cases", "bug tracking"]},
#     "api testing with postman": {"skills": ["api testing", "postman", "http methods"]},
#     "automation testing with selenium": {"skills": ["selenium", "test automation", "webdriver"]},
# }
# suggested_path = ["manual testing foundations", "api testing with postman", "automation testing with selenium"]

# metrics = evaluate_path(
#     jd_skills,
#     courses,
#     suggested_path,
#     k=5,
#     manual_rubric={"relevance": 5, "feasibility": 4, "clarity": 4}
# )

# print(metrics)
