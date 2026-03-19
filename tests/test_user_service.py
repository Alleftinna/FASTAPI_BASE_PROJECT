from unittest.mock import AsyncMock

import pytest

from src.services.user_service import UserService
from src.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_success() -> None:
    session = AsyncMock()
    service = UserService(session=session)

    repository = AsyncMock()
    repository.get_by_email.return_value = None
    repository.add.return_value = AsyncMock()
    service.user_repository = repository

    payload = UserCreate(email="user@example.com", full_name="Test User")
    created = await service.create_user(payload)

    assert created is repository.add.return_value
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email() -> None:
    session = AsyncMock()
    service = UserService(session=session)

    repository = AsyncMock()
    repository.get_by_email.return_value = object()
    service.user_repository = repository

    payload = UserCreate(email="dupe@example.com", full_name="Duplicate")

    with pytest.raises(ValueError, match="already exists"):
        await service.create_user(payload)
