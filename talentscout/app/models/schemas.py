from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from fastapi_users import schemas
import uuid

# User Schemas for FastAPI Users
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class RoleSpec(BaseModel):
    title: str
    required_skills: List[str]
    nice_to_have: List[str]
    experience_years_min: int
    experience_years_max: int
    location_preference: str
    team_size: Optional[str] = None
    culture_signals: List[str]
    raw_jd: str

class CandidateList(BaseModel):
    url: str
    source: str # "github", "linkedin", "naukri", "twitter"
    basic_info: Optional[Dict[str, Any]] = None

class GithubSignal(BaseModel):
    total_repos: int
    public_contributions_1y: int
    notable_repos: List[str]
    primary_languages: List[str]
    code_quality_summary: str

class CandidateProfile(BaseModel):
    name: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    naukri_url: Optional[str] = None
    twitter_url: Optional[str] = None
    current_role: str = "Unknown"
    years_experience: float = 0.0
    skills_confirmed: List[str] = []
    github_signal: Optional[GithubSignal] = None
    writing_samples: List[str] = []
    communication_quality: str = "limited_signal"
    red_flags: List[str] = []

class CandidateBrief(BaseModel):
    rank: int
    profile: CandidateProfile
    overall_score: float
    score_breakdown: Dict[str, float]
    why_strong: List[str]
    concerns: List[str]
    fit_summary: str
    suggested_questions: List[str]
    sources: List[str]
