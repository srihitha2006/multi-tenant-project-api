import json
from app.services.cache import cache_get, cache_set, cache_key
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.dependencies.auth import require_role
from app.dependencies.current_user import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, dependencies=[Depends(require_role(["Admin", "Manager"]))])
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user()),
):
    # Force org_id from token (multi-tenancy)
    org_id = user["org_id"]

    project = Project(
    name=data.name,
    organization_id=user["org_id"]
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project



@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user()),
):
    org_id = user["org_id"]
    key = cache_key("projects", org_id, skip, limit)

    cached = await cache_get(key)
    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Project)
        .where(Project.organization_id == org_id)
        .offset(skip)
        .limit(limit)
    )
    projects = result.scalars().all()

    data = [{"id": p.id, "name": p.name, "organization_id": p.organization_id} for p in projects]

    await cache_set(key, data, ttl=60)
    return data



@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user()),
):
    org_id = user["org_id"]
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.organization_id == org_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["Admin"]))])
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user()),
):
    org_id = user["org_id"]
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.organization_id == org_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
    return None
