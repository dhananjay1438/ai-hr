from app.agents.base import BaseAgent
from app.models.schemas import CandidateProfile, RoleSpec
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ScoredOutput(BaseModel):
    overall_score: float = Field(description="Score from 0.0 to 10.0")
    score_breakdown: Dict[str, float] = Field(description="Keys must include 'technical', 'communication', 'startup_fit'")
    why_strong: List[str] = Field(description="2-3 concrete strengths")
    concerns: List[str] = Field(description="Honest concerns")
    fit_summary: str = Field(description="2-3 sentence narrative for founder")
    suggested_questions: List[str] = Field(description="Interview questions tailored to concerns")

class FitScorerAgent(BaseAgent):
    def score(self, profiles: List[CandidateProfile], role_spec: RoleSpec) -> List[Dict[str, Any]]:
        parser = JsonOutputParser(pydantic_object=ScoredOutput)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical hiring manager evaluating a candidate against a job description. Be honest and critical. Output JSON as specified: \n{format_instructions}"),
            ("user", "Job Specification:\n{role_spec}\n\nCandidate Profile:\n{profile}")
        ])

        prompt = prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | self.llm | parser

        scored_profiles = []
        for p in profiles:
            try:
                # LLM Invocation
                result = chain.invoke({
                    "role_spec": role_spec.model_dump_json(),
                    "profile": p.model_dump_json()
                })

                scored_profiles.append({
                    "profile": p,
                    "scores": result
                })
            except Exception as e:
                print(f"Scoring failed for {p.name}: {e}")
                # Provide default scoring if LLM fails
                scored_profiles.append({
                    "profile": p,
                    "scores": {
                        "overall_score": 5.0,
                        "score_breakdown": {"technical": 5.0, "communication": 5.0, "startup_fit": 5.0},
                        "why_strong": [],
                        "concerns": ["Scoring agent failed."],
                        "fit_summary": "Could not generate summary.",
                        "suggested_questions": []
                    }
                })

        return scored_profiles
