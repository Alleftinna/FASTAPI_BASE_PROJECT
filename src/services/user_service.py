from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate


class UserService:
    """Сервисный слой для бизнес-логики пользователей."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session=session)

    async def create_user(self, payload: UserCreate) -> User:
        existing_user = await self.user_repository.get_by_email(payload.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        new_user = User(email=payload.email, full_name=payload.full_name)
        created_user = await self.user_repository.add(new_user)
        await self.session.commit()
        return created_user

    async def list_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        return await self.user_repository.list(limit=limit, offset=offset)
