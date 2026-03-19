from fastapi import status

from src.exceptions.base import BaseException


class UserException(BaseException):
    """Базовый класс для исключений, связанных с пользователями."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""


class UserAlreadyExists(UserException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, email: str) -> None:
        self.detail = f"Пользователь с email={email} уже существует."
        super().__init__()
