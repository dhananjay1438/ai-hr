from app.models.schemas import CandidateBrief
from typing import List, Dict, Any

class ReportGeneratorAgent:
    def generate(self, scored_profiles: List[Dict[str, Any]]) -> List[CandidateBrief]:
        # Sort by overall score descending
        scored_profiles.sort(key=lambda x: x["scores"].get("overall_score", 0), reverse=True)

        briefs = []
        for i, item in enumerate(scored_profiles):
            profile = item["profile"]
            scores = item["scores"]

            sources = []
            if profile.github_url: sources.append(profile.github_url)
            if profile.linkedin_url: sources.append(profile.linkedin_url)
            if profile.naukri_url: sources.append(profile.naukri_url)
            if profile.twitter_url: sources.append(profile.twitter_url)

            briefs.append(CandidateBrief(
                rank=i + 1,
                profile=profile,
                overall_score=scores.get("overall_score", 0.0),
                score_breakdown=scores.get("score_breakdown", {}),
                why_strong=scores.get("why_strong", []),
                concerns=scores.get("concerns", []),
                fit_summary=scores.get("fit_summary", ""),
                suggested_questions=scores.get("suggested_questions", []),
                sources=sources
            ))

        return briefs
