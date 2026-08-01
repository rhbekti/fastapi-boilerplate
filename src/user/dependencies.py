from typing import Annotated
from fastapi import Depends

from src.user.service import UserService
from src.core.dependencies import SessionDep


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
