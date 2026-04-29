from app.agents.base import BaseAgent
from app.models.schemas import CandidateList, CandidateProfile, GithubSignal
from app.scrapers.github import GitHubScraper
from app.scrapers.linkedin import LinkedInScraper
from app.scrapers.twitter import TwitterScraper
import asyncio
from typing import List

class DeepProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        from app.config import settings
        self.github_scraper = GitHubScraper(token=settings.github_token.get_secret_value() if settings.github_token else None)
        self.linkedin_scraper = LinkedInScraper(email=settings.linkedin_email, password=settings.linkedin_password.get_secret_value() if settings.linkedin_password else None)
        self.twitter_scraper = TwitterScraper(bearer_token=settings.twitter_bearer_token.get_secret_value() if settings.twitter_bearer_token else None)

    async def enrich(self, candidates: List[CandidateList]) -> List[CandidateProfile]:
        profiles = []

        for c in candidates:
            profile_data = {
                "name": c.basic_info.get("name") or c.basic_info.get("username") or "Unknown",
            }

            if c.source == "github":
                username = c.basic_info.get("username")
                if username:
                    gh_details = self.github_scraper.get_user_profile(username)
                    profile_data["github_url"] = gh_details.get("url")

                    langs = list(set([r["language"] for r in gh_details.get("top_repos", []) if r["language"]]))
                    notable = [r["name"] for r in gh_details.get("top_repos", []) if r.get("stars", 0) > 0]

                    # Call LLM to summarize code quality (mocked logic for POC)
                    code_quality_summary = "Adequate structure and activity."
                    if notable:
                        code_quality_summary = f"Maintains repos like {', '.join(notable[:2])}."

                    profile_data["github_signal"] = GithubSignal(
                        total_repos=gh_details.get("public_repos", 0),
                        public_contributions_1y=0, # Need GraphQL API for this, skipping for POC
                        notable_repos=notable,
                        primary_languages=langs,
                        code_quality_summary=code_quality_summary
                    )
            elif c.source == "linkedin":
                profile_data["linkedin_url"] = c.url
                linkedin_details = await self.linkedin_scraper.get_profile(c.url)
                if linkedin_details.get("name") and linkedin_details.get("name") != "Unknown":
                    profile_data["name"] = linkedin_details["name"]
                if linkedin_details.get("headline"):
                    profile_data["current_role"] = linkedin_details["headline"]
            elif c.source == "naukri":
                profile_data["naukri_url"] = c.url
            elif c.source == "twitter":
                profile_data["twitter_url"] = c.url

            profiles.append(CandidateProfile(**profile_data))

        return profiles
