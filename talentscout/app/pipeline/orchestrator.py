from app.models.schemas import RoleSpec, CandidateBrief
from app.agents.jd_parser import JDParserAgent
from app.agents.scout import ScoutAgent
from app.agents.filter import FilterAgent
from app.agents.deep_profile import DeepProfileAgent
from app.agents.fit_scorer import FitScorerAgent
from app.agents.report_generator import ReportGeneratorAgent
import asyncio
from typing import List

class PipelineOrchestrator:
    def __init__(self):
        self.jd_parser = JDParserAgent()
        self.scout = ScoutAgent()
        self.filter_agent = FilterAgent()
        self.deep_profile = DeepProfileAgent()
        self.fit_scorer = FitScorerAgent()
        self.report_generator = ReportGeneratorAgent()

    async def run(self, raw_jd: str) -> List[CandidateBrief]:
        print("1. Parsing JD...")
        role_spec = self.jd_parser.parse(raw_jd)

        print("2. Scouting candidates...")
        raw_candidates = await self.scout.search(role_spec)

        print("3. Filtering candidates...")
        filtered_candidates = self.filter_agent.filter(raw_candidates, role_spec)

        print("4. Deep profiling...")
        enriched_profiles = await self.deep_profile.enrich(filtered_candidates)

        print("5. Scoring candidates...")
        scored_profiles = self.fit_scorer.score(enriched_profiles, role_spec)

        print("6. Generating report...")
        briefs = self.report_generator.generate(scored_profiles)

        return briefs
