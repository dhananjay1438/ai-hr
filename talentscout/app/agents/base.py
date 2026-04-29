from langchain_google_vertexai import ChatVertexAI
from app.config import settings

class BaseAgent:
    def __init__(self):
        # We assume GOOGLE_APPLICATION_CREDENTIALS is set in config.py
        self.llm = ChatVertexAI(
            model_name=settings.vertexai_model,
            project=settings.google_cloud_project,
            location=settings.google_cloud_region,
            temperature=0.2
        )
