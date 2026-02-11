from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.task import Task
from app.services.email import send_task_email

router = APIRouter(prefix="/overdue", tags=["Overdue"])

@router.post("/check")
async def check_overdue(db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()

    result = await db.execute(
        select(Task).where(
            Task.due_date != None,
            Task.due_date < now,
            Task.completed == False
        )
    )
    tasks = result.scalars().all()

    for t in tasks:
        if t.assigned_to_email:
            send_task_email(t.assigned_to_email, f"OVERDUE: {t.title}")

    return {"overdue_count": len(tasks)}
