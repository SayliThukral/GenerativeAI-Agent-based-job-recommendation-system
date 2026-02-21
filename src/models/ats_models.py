from pydantic import BaseModel, Field
from typing import List, Optional


class GapAnalysis(BaseModel):
    missing_skill: str
    importance_level: str = Field(description="High, Medium, or Low")
    youtube_search_query: str = Field(description="Optimized query for Serper API")

class ATSResult(BaseModel):
    match_score: int = Field(ge=0, le=100)
    strengths: List[str]
    gaps: List[GapAnalysis]
    youtube_recommendations: Optional[List[dict]] = []
