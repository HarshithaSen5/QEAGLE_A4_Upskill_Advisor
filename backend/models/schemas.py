#schemas
from pydantic import BaseModel
from typing import List

class SkillRequest(BaseModel):
    role: str
    skills: List[str]

class SkillGapResponse(BaseModel):
    missing_skills: List[str]
    recommended_courses: List[str]
    learning_path: List[str]