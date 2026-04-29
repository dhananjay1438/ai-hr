from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_async_session, current_active_user
from app.models.db import User, Report, Role
from app.models.schemas import CandidateBrief
from typing import List
import uuid
import json

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/{role_id}", response_model=List[CandidateBrief])
async def get_report(
    role_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    role = await session.get(Role, role_id)
    if not role or role.user_id != user.id:
         raise HTTPException(status_code=404, detail="Role not found")

    result = await session.execute(select(Report).where(Report.role_id == role_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not ready or not found")

    return report.data

@router.get("/{role_id}/pdf")
async def get_report_pdf(
    role_id: uuid.UUID,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    from app.utils.pdf_generator import generate_brief_pdf
    from PyPDF2 import PdfMerger
    import io

    role = await session.get(Role, role_id)
    if not role or role.user_id != user.id:
         raise HTTPException(status_code=404, detail="Role not found")

    result = await session.execute(select(Report).where(Report.role_id == role_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not ready or not found")

    briefs = [CandidateBrief(**b) for b in report.data]
    merger = PdfMerger()

    for brief in briefs:
        pdf_bytes = generate_brief_pdf(brief)
        merger.append(io.BytesIO(pdf_bytes))

    output = io.BytesIO()
    merger.write(output)
    merger.close()

    return Response(content=output.getvalue(), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=report_{role_id}.pdf"
    })
