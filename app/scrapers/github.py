import os
from github import Github, Auth
from typing import List, Dict, Any

class GitHubScraper:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if self.token:
            auth = Auth.Token(self.token)
            self.client = Github(auth=auth)
        else:
            self.client = Github()

    def search_candidates(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for users matching a specific query (e.g. 'language:python location:India').
        Returns basic user info.
        """
        users = self.client.search_users(query)
        results = []
        for i, user in enumerate(users):
            if i >= limit:
                break
            results.append({
                "username": user.login,
                "name": user.name,
                "url": user.html_url,
                "location": user.location,
                "bio": user.bio,
                "followers": user.followers,
                "public_repos": user.public_repos
            })
        return results

    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetch detailed user profile for deep profiling.
        """
        user = self.client.get_user(username)

        # Get repos
        repos = user.get_repos(type="owner", sort="updated", direction="desc")
        repo_data = []
        for i, repo in enumerate(repos):
            if i >= 10: # Only fetch top 10 recent repos
                break
            repo_data.append({
                "name": repo.name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
            })

        return {
            "username": user.login,
            "name": user.name,
            "url": user.html_url,
            "location": user.location,
            "bio": user.bio,
            "company": user.company,
            "blog": user.blog,
            "followers": user.followers,
            "public_repos": user.public_repos,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "top_repos": repo_data
        }
