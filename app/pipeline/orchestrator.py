from app.models.schemas import RoleSpec, CandidateBrief
from app.factories.agent_factory import AgentFactory
from typing import List

class PipelineOrchestrator:
    def __init__(self):
        self.jd_parser = AgentFactory.create_jd_parser()
        self.scout = AgentFactory.create_scout()
        self.filter_agent = AgentFactory.create_filter()
        self.deep_profile = AgentFactory.create_deep_profile()
        self.fit_scorer = AgentFactory.create_fit_scorer()
        self.report_generator = AgentFactory.create_report_generator()

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
