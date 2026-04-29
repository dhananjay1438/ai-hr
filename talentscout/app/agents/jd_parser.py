from app.agents.base import BaseAgent
from app.models.schemas import RoleSpec
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class JDParserAgent(BaseAgent):
    def parse(self, raw_jd: str) -> RoleSpec:
        parser = PydanticOutputParser(pydantic_object=RoleSpec)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical recruiter. Extract the following information from the job description.\n{format_instructions}"),
            ("user", "Job Description:\n{raw_jd}")
        ])

        prompt = prompt.partial(format_instructions=parser.get_format_instructions())
        chain = prompt | self.llm | parser

        # Inject the raw jd back into the parsed object
        parsed = chain.invoke({"raw_jd": raw_jd})
        parsed.raw_jd = raw_jd
        return parsed
