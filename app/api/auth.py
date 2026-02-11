from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# -------- Request schema --------
class LoginRequest(BaseModel):
    email: str
    role: str   # Admin / Manager / Member
    org_id: int


# -------- Response schema --------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------- Login API --------
@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    if data.role not in ["Admin", "Manager", "Member"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    token = create_access_token({
        "sub": data.email,
        "role": data.role,
        "org_id": data.org_id
    })

    return {"access_token": token}
