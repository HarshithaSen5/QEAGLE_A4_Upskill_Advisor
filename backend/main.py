#main.py
# --- Imports and setup ---
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import SkillRequest, SkillGapResponse
from pydantic import BaseModel
# from services.metrics import evaluate_path
from typing import Dict, List, Optional
try:
    from services.gap_analyzer import analyze_gap
    from services.planner import plan_courses
    from services.retriever import load_courses, load_job_description, keyword_search
    from services.llm_service import LLMService
    from services.minilm_service import MiniLMService
except ImportError:
    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from services.gap_analyzer import analyze_gap
    from services.planner import plan_courses
    from services.retriever import load_courses, load_job_description, keyword_search
    from services.llm_service import LLMService
    from services.minilm_service import MiniLMService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize LLM and MiniLM services for Ollama (local model)
llm_service = LLMService(
    model_name="phi3",  # or another small model name
    endpoint="http://localhost:11434/api/generate"
)
minilm_service = MiniLMService()
from pydantic import BaseModel

# Request/response models for RAG+LLM

# Updated request model to include user_skills
class RAGLLMRequest(BaseModel):
    role: str
    user_skills: list


# Updated response model to include missing_skills and recommended_courses

# Updated response model to include course descriptions
from typing import List, Dict
from typing import List
class CourseInfo(BaseModel):
    name: str
    description: str
    timeline: str = ""
    difficulty: str = ""
    prerequisites: List[str] = []
    outcomes: List[str] = []

class RAGLLMResponse(BaseModel):
    answer: str
    missing_skills: list
    recommended_courses: List[CourseInfo]



@app.post("/rag-llm", response_model=RAGLLMResponse)
def rag_llm(request: RAGLLMRequest):
    # 1. Compute missing skills
    from services.gap_analyzer import analyze_gap
    missing_skills = analyze_gap(request.role, request.user_skills)
    
    # 2. Plan recommended courses
    from services.planner import plan_courses
    recommended_course_names = plan_courses(missing_skills)[:3]
    
    # 3. Get course descriptions
    courses_data = load_courses()
    recommended_courses = []
    for name in recommended_course_names:
        course = courses_data.get(name, {})
        duration = course.get("duration_weeks")
        timeline = f"{duration} weeks" if duration else ""
        difficulty = course.get("difficulty", "")
        prerequisites = course.get("prerequisites", [])
        if isinstance(prerequisites, str):
            prerequisites = [prerequisites]
        outcomes = course.get("outcomes", [])
        if isinstance(outcomes, str):
            outcomes = [outcomes]
        recommended_courses.append(CourseInfo(
            name=name,
            description=course.get("description", ""),
            timeline=timeline,
            difficulty=difficulty,
            prerequisites=prerequisites,
            outcomes=outcomes
        ))
    
    # Sort courses: Beginner first, then Intermediate, then Advanced
    difficulty_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
    recommended_courses.sort(key=lambda c: difficulty_order.get(c.difficulty.lower(), 99))
    
    # Ensure at least 3 courses are recommended
    if len(recommended_courses) < 3:
        additional_courses = [
            CourseInfo(
                name=name,
                description=course.get("description", ""),
                timeline=f"{course.get('duration_weeks', '')} weeks" if course.get('duration_weeks') else "",
                difficulty=course.get("difficulty", ""),
                prerequisites=course.get("prerequisites", []) if isinstance(course.get("prerequisites"), list) else [course.get("prerequisites", "")],
                outcomes=course.get("outcomes", []) if isinstance(course.get("outcomes"), list) else [course.get("outcomes", "")]
            )
            for name, course in courses_data.items()
            if name not in recommended_course_names
        ]
        additional_courses.sort(key=lambda c: difficulty_order.get(c.difficulty.lower(), 99))
        recommended_courses.extend(additional_courses[:3 - len(recommended_courses)])
    
    # 4. Prepare prompt for LLM
    max_skills = 5
    max_courses = 3
    limited_missing_skills = missing_skills[:max_skills]
    limited_recommended_courses = recommended_course_names[:max_courses]

    prompt = (
        f"Role: {request.role}\n"
        f"User skills: {', '.join(request.user_skills)}\n"
        f"Missing skills: {', '.join(limited_missing_skills)}\n"
        f"Recommended courses: {', '.join(limited_recommended_courses)}\n"
    )
    answer = llm_service.generate(prompt)
    if not answer:
        answer = minilm_service.generate(prompt)
    
    # Shorten the LLM response
    def shorten_answer(answer: str, max_sentences: int = 2) -> str:
        sentences = answer.split('. ')
        return '.'.join(sentences[:max_sentences]) + ('.' if len(sentences) > max_sentences else '')

    shortened_answer = shorten_answer(answer, max_sentences=2)

    # Normalize difficulty levels to lowercase for all courses
    for course in recommended_courses:
        course.difficulty = course.difficulty.lower()

    # Re-sort courses after appending additional ones
    recommended_courses.sort(key=lambda c: difficulty_order.get(c.difficulty, 99))

    # Filter out courses that match the user's existing skills
    user_skills_lower = [skill.lower() for skill in request.user_skills]
    filtered_courses = [
        course for course in recommended_courses
        if not any(skill.lower() in user_skills_lower for skill in course.prerequisites)
    ]

    # Ensure at least 3 courses are recommended after filtering
    if len(filtered_courses) < 3:
        additional_courses = [
            CourseInfo(
                name=name,
                description=course.get("description", ""),
                timeline=f"{course.get('duration_weeks', '')} weeks" if course.get('duration_weeks') else "",
                difficulty=course.get("difficulty", ""),
                prerequisites=course.get("prerequisites", []) if isinstance(course.get("prerequisites"), list) else [course.get("prerequisites", "")],
                outcomes=course.get("outcomes", []) if isinstance(course.get("outcomes"), list) else [course.get("outcomes", "")]
            )
            for name, course in courses_data.items()
            if name not in [c.name for c in filtered_courses]
        ]
        additional_courses.sort(key=lambda c: difficulty_order.get(c.difficulty.lower(), 99))
        filtered_courses.extend(additional_courses[:3 - len(filtered_courses)])

    recommended_courses = filtered_courses

    # Improved formatting for complete sentences and chat-like style
    def format_answer_chatgpt_style(answer: str, max_points: int = 3) -> str:  # Limit to 3 points
        import re
        # Split by numbered points, dashes, or newlines
        points = re.split(r'\n\s*\d+\.\s*|\n\s*-\s*|\n', answer)
        points = [p.strip() for p in points if p.strip()]
        # If the answer is a single paragraph, split by sentences
        if len(points) == 1:
            points = re.split(r'(?<=[.!?])\s+', answer)
        # Remove markdown and excessive whitespace
        cleaned_points = []
        for p in points:
            p = re.sub(r'\*\*|__|\*', '', p)
            p = re.sub(r'\s+', ' ', p)
            # Do not truncate, keep full sentences
            cleaned_points.append(p)
        cleaned_points = cleaned_points[:max_points]  # Limit to max_points
        # Format like ChatGPT: numbered list with full sentences
        return '\n'.join(f"{i+1}. {p}" for i, p in enumerate(cleaned_points) if p)

    # Use the updated function to format the LLM response
    formatted_answer = format_answer_chatgpt_style(answer, max_points=3)  # Limit to 3 points

    return RAGLLMResponse(
        answer=formatted_answer,
        missing_skills=missing_skills,
        recommended_courses=recommended_courses
    )

@app.get("/")
def home():
    return {"message": "Upskill Advisor API running "}

@app.post("/analyze", response_model=SkillGapResponse)
def analyze(request: SkillRequest):
    missing = analyze_gap(request.role, request.skills)
    courses = plan_courses(missing)
    return SkillGapResponse(
        missing_skills=missing,
        recommended_courses=courses,
        learning_path=courses  
    )

@app.get("/course/{course_id}")
def get_course(course_id: str):
    """Fetch metadata for a specific course"""
    courses = load_courses()

    course_map = {k.lower(): v for k, v in courses.items()}
    course = course_map.get(course_id.lower())

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"id": course_id, **course}