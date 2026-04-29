from app.factories.llm_factory import LLMFactory

class BaseAgent:
    def __init__(self):
        # We assume GOOGLE_APPLICATION_CREDENTIALS is set in config.py
        self.llm = LLMFactory.create_vertex_chat(temperature=0.2)
