from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    project_id: int
    due_date: Optional[datetime] = None
    assigned_to_email: Optional[str] = None



class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    project_id: int

    class Config:
        from_attributes = True
