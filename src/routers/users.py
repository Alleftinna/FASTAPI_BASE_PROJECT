from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.schemas.user import UserCreate, UserRead
from src.services.user_service import UserService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    service = UserService(session=session)
    user = await service.create_user(payload)
    return UserRead.model_validate(user)


@users_router.get("", response_model=list[UserRead])
async def list_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = 100,
    offset: int = 0,
) -> list[UserRead]:
    service = UserService(session=session)
    users = await service.list_users(limit=limit, offset=offset)
    return [UserRead.model_validate(user) for user in users]
