from pydantic import BaseModel, Field
from typing import List, Optional

class WorkExperience(BaseModel):
    company: str
    role: str
    duration: str
    achievements: List[str]

class CVParsedData(BaseModel):
    contact_info: dict
    skills_technical: List[str]
    skills_soft: List[str]
    experience: List[WorkExperience]
    education: List[dict]


