from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os

class Settings(BaseSettings):
    # Google Vertex AI
    google_cloud_project: str = ""
    google_cloud_region: str = "us-central1"
    vertexai_model: str = "gemini-1.5-pro"

    # Optional credentials JSON
    google_application_credentials: str | None = None

    # GitHub
    github_token: SecretStr | None = None

    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/talentscout"
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    secret_key: SecretStr = SecretStr("insecure-dev-key")

    # LinkedIn
    linkedin_email: str | None = None
    linkedin_password: SecretStr | None = None

    # Twitter
    twitter_bearer_token: SecretStr | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

# Check for credentials.json fallback for Vertex AI
if not settings.google_application_credentials and os.path.exists("credentials.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("credentials.json")
    settings.google_application_credentials = os.path.abspath("credentials.json")
elif settings.google_application_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
