import json
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.cache import cache_get, cache_set, cache_key
from app.services.email import send_task_email
from app.dependencies.current_user import get_current_user
from app.models.project import Project
from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.dependencies.auth import require_role

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ✅ CREATE task (triggers background email)
@router.post("/", status_code=201)
async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    new_task = Task(
    title=task.title,
    completed=False,
    project_id=task.project_id,
    due_date=task.due_date,
    assigned_to_email=task.assigned_to_email
)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    to_email = task.assigned_to_email or "user@example.com"

    background_tasks.add_task(
    send_task_email,
    to_email,
    new_task.title
)

    return new_task


# ✅ LIST tasks (cached + org filtered)
@router.get("/")
async def list_tasks(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    org_id = user["org_id"]
    key = cache_key("tasks", org_id, skip, limit)

    cached = await cache_get(key)
    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.organization_id == org_id)
        .offset(skip)
        .limit(limit)
    )
    tasks = result.scalars().all()

    data = [
        {"id": t.id, "title": t.title, "completed": t.completed, "project_id": t.project_id}
        for t in tasks
    ]

    await cache_set(key, data, ttl=60)
    return data


# ✅ GET single task
@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# ✅ UPDATE task (Admin/Manager)
@router.put("/{task_id}", dependencies=[Depends(require_role(["Admin", "Manager"]))])
async def update_task(task_id: int, data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    if data.completed is not None:
        task.completed = data.completed

    await db.commit()
    await db.refresh(task)
    return task


# ✅ DELETE task (Admin only)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(["Admin"]))])
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return None
