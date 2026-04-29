from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_async_session, current_active_user
from app.models.db import User, Role
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/roles", tags=["roles"])

class RoleCreate(BaseModel):
    raw_jd: str

class RoleResponse(BaseModel):
    id: uuid.UUID
    status: str

@router.post("", response_model=RoleResponse)
async def create_role(
    role_in: RoleCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    role = Role(user_id=user.id, raw_jd=role_in.raw_jd)
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    role = await session.get(Role, role_id)
    if not role or role.user_id != user.id:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
