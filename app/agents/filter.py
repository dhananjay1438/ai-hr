from app.agents.base import BaseAgent
from app.models.schemas import CandidateList, RoleSpec
from typing import List

class FilterAgent(BaseAgent):
    def filter(self, candidates: List[CandidateList], role_spec: RoleSpec) -> List[CandidateList]:
        # Quick pass: Deduplicate and basic scoring.
        # For POC, we'll just deduplicate by URL and return the top 10.
        seen_urls = set()
        filtered = []
        for c in candidates:
            if c.url not in seen_urls:
                seen_urls.add(c.url)
                filtered.append(c)

        # Limit to top 10 for deep profiling
        return filtered[:10]
