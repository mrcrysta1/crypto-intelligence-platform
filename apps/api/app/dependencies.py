from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session

security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    if credentials is None:
        return {"user_id": None, "username": "anonymous"}

    token = credentials.credentials

    try:
        from jose import JWTError, jwt

        from app.config import settings

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: Optional[str] = payload.get("sub")
        username: Optional[str] = payload.get("username")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {"user_id": user_id, "username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    except ImportError:
        return {"user_id": None, "username": "anonymous"}
