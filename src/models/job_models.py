from pydantic import BaseModel, Field
from typing import List, Optional

class UserSettings(BaseModel):
    target_role: str
    location_preference: str = "Remote"
    min_salary: Optional[int]
    date_posted: str = "past_week"

class JobRecommendation(BaseModel):
    job_title: str
    company: str
    apply_link: str
    match_reason: str
