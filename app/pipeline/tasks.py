import asyncio
from celery import Celery
from app.config import settings
from app.pipeline.orchestrator import PipelineOrchestrator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.db import Role, Report
from pydantic import TypeAdapter
from typing import List
from app.models.schemas import CandidateBrief

celery_app = Celery("talentscout", broker=settings.redis_url, backend=settings.redis_url)

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def _run_pipeline_async(role_id_str: str):
    async with async_session() as session:
        role = await session.get(Role, role_id_str)
        if not role:
            return

        role.status = "RUNNING"
        await session.commit()

        try:
            orchestrator = PipelineOrchestrator()
            briefs = await orchestrator.run(role.raw_jd)

            # Serialize
            adapter = TypeAdapter(List[CandidateBrief])
            briefs_dict = adapter.dump_python(briefs, mode="json")

            report = Report(role_id=role.id, data=briefs_dict)
            session.add(report)

            role.status = "DONE"
            await session.commit()
        except Exception as e:
            print(f"Pipeline failed: {e}")
            role.status = "FAILED"
            await session.commit()

@celery_app.task
def run_pipeline(role_id_str: str):

    asyncio.run(_run_pipeline_async(role_id_str))
