from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.organization import router as organization_router
from app.api.task import router as task_router
from app.api.project import router as project_router
from app.api.overdue import router as overdue_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(organization_router)
app.include_router(task_router)
app.include_router(project_router)
app.include_router(overdue_router)
