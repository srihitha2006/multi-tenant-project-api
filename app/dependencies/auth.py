from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def require_role(required_roles: list[str]):
    async def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        from jose import jwt, JWTError
        from app.core.security import SECRET_KEY, ALGORITHM
        from fastapi import HTTPException, status

        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        role = (payload.get("role") or "").lower()
        allowed = [r.lower() for r in required_roles]

        if role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")


        return payload

    return role_checker
