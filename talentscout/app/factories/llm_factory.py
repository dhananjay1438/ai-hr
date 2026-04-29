from langchain_google_vertexai import ChatVertexAI

from app.config import settings


class LLMFactory:
    """Factory for creating configured LLM clients."""

    @staticmethod
    def create_vertex_chat(temperature: float = 0.2) -> ChatVertexAI:
        return ChatVertexAI(
            model_name=settings.vertexai_model,
            project=settings.google_cloud_project,
            location=settings.google_cloud_region,
            temperature=temperature,
        )
