from app.agents.deep_profile import DeepProfileAgent
from app.agents.filter import FilterAgent
from app.agents.fit_scorer import FitScorerAgent
from app.agents.jd_parser import JDParserAgent
from app.agents.report_generator import ReportGeneratorAgent
from app.agents.scout import ScoutAgent


class AgentFactory:
    """Factory for assembling pipeline agents."""

    @staticmethod
    def create_jd_parser() -> JDParserAgent:
        return JDParserAgent()

    @staticmethod
    def create_scout() -> ScoutAgent:
        return ScoutAgent()

    @staticmethod
    def create_filter() -> FilterAgent:
        return FilterAgent()

    @staticmethod
    def create_deep_profile() -> DeepProfileAgent:
        return DeepProfileAgent()

    @staticmethod
    def create_fit_scorer() -> FitScorerAgent:
        return FitScorerAgent()

    @staticmethod
    def create_report_generator() -> ReportGeneratorAgent:
        return ReportGeneratorAgent()
