from pydantic import BaseModel, Field

class Section(BaseModel):
    score: int = Field(default=0, ge=0, le=20)
    details: str = ""

class Analysis(BaseModel):
    personality: Section = Field(default_factory=Section)
    lifestyle: Section = Field(default_factory=Section)
    family_values: Section = Field(default_factory=Section)
    emotional: Section = Field(default_factory=Section)
    strengths_challenges: Section = Field(default_factory=Section)

class MarriageMatchResponse(BaseModel):
    compatibility_score: int = Field(ge=0, le=100)
    analysis: Analysis
    kundli_match: str
    recommendation: str
