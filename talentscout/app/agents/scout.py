from app.agents.base import BaseAgent
from app.models.schemas import RoleSpec, CandidateList
from app.scrapers.github import GitHubScraper
from app.scrapers.linkedin import LinkedInScraper
from app.scrapers.naukri import NaukriScraper
from app.scrapers.twitter import TwitterScraper
import asyncio
from typing import List

class ScoutAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        from app.config import settings
        self.github_scraper = GitHubScraper(token=settings.github_token.get_secret_value() if settings.github_token else None)
        self.linkedin_scraper = LinkedInScraper(email=settings.linkedin_email, password=settings.linkedin_password.get_secret_value() if settings.linkedin_password else None)
        self.naukri_scraper = NaukriScraper()
        self.twitter_scraper = TwitterScraper(bearer_token=settings.twitter_bearer_token.get_secret_value() if settings.twitter_bearer_token else None)

    async def search(self, role_spec: RoleSpec) -> List[CandidateList]:
        # Simple heuristic search queries based on JD
        # In a real app, an LLM might generate these queries

        candidates = []

        # 1. GitHub Search
        skills_query = " ".join(role_spec.required_skills[:3])
        location_query = role_spec.location_preference if role_spec.location_preference.lower() != "remote" else ""
        gh_query = f"{skills_query} location:{location_query}" if location_query else skills_query

        gh_results = self.github_scraper.search_candidates(gh_query, limit=10)
        for res in gh_results:
            candidates.append(CandidateList(url=res['url'], source="github", basic_info=res))

        # 2. LinkedIn Search (async)
        linkedin_results = await self.linkedin_scraper.search_candidates(skills_query)
        for res in linkedin_results:
            candidates.append(CandidateList(url=res['url'], source="linkedin", basic_info=res))

        # 3. Naukri Mock Search (async)
        naukri_results = await self.naukri_scraper.search_candidates(skills_query, location_query)
        for res in naukri_results:
             candidates.append(CandidateList(url=res['url'], source="naukri", basic_info=res))

        # 4. Twitter Mock Search
        tw_results = self.twitter_scraper.search_users(skills_query, limit=5)
        for res in tw_results:
            candidates.append(CandidateList(url=res['url'], source="twitter", basic_info=res))

        return candidates
