import tweepy
from typing import List, Dict, Any
import os

class TwitterScraper:
    def __init__(self, bearer_token: str | None = None):
        self.bearer_token = bearer_token or os.environ.get("TWITTER_BEARER_TOKEN")
        if self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        else:
            self.client = None

    def search_users(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.client:
            print("Twitter bearer token not provided. Skipping search.")
            return []

        try:
            # We search for recent tweets matching the query and extract users
            response = self.client.search_recent_tweets(
                query=f"{query} -is:retweet",
                expansions=["author_id"],
                user_fields=["description", "location", "public_metrics"],
                max_results=limit
            )

            if not response.data:
                return []

            users_dict = {u.id: u for u in response.includes['users']}
            results = []

            # Use a set to deduplicate users
            seen_users = set()

            for tweet in response.data:
                user = users_dict[tweet.author_id]
                if user.id not in seen_users:
                    seen_users.add(user.id)
                    results.append({
                        "username": user.username,
                        "name": user.name,
                        "description": user.description,
                        "location": user.location,
                        "url": f"https://twitter.com/{user.username}",
                        "followers": user.public_metrics["followers_count"]
                    })
                    if len(results) >= limit:
                        break

            return results
        except Exception as e:
            print(f"Error searching Twitter: {e}")
            return []

    def get_user_profile(self, username: str) -> Dict[str, Any]:
        if not self.client:
             return {"username": username, "error": "No bearer token"}

        try:
            user = self.client.get_user(
                username=username,
                user_fields=["description", "location", "public_metrics", "url", "created_at"]
            )
            if not user.data:
                return {"username": username, "error": "User not found"}

            u = user.data
            return {
                "username": u.username,
                "name": u.name,
                "description": u.description,
                "location": u.location,
                "url": f"https://twitter.com/{u.username}",
                "website": u.url,
                "followers": u.public_metrics["followers_count"],
                "following": u.public_metrics["following_count"],
                "tweet_count": u.public_metrics["tweet_count"],
            }
        except Exception as e:
            print(f"Error getting Twitter profile for {username}: {e}")
            return {"username": username, "error": str(e)}
