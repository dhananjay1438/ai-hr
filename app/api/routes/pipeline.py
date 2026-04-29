from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_async_session, current_active_user
from app.models.db import User, Role
from app.pipeline.tasks import run_pipeline
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

class PipelineRunResponse(BaseModel):
    run_id: str # celery task id

class PipelineStatusResponse(BaseModel):
    status: str

@router.post("/run", response_model=PipelineRunResponse)
async def trigger_pipeline(
    role_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    role = await session.get(Role, role_id)
    if not role or role.user_id != user.id:
        raise HTTPException(status_code=404, detail="Role not found")

    task = run_pipeline.delay(str(role.id))
    return {"run_id": task.id}

@router.get("/{run_id}/status", response_model=PipelineStatusResponse)
async def get_pipeline_status(
    run_id: str,
    user: User = Depends(current_active_user)
):
    from app.pipeline.tasks import celery_app
    res = celery_app.AsyncResult(run_id)
    return {"status": res.status}
