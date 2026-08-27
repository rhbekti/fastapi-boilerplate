from typing import Annotated

from fastapi import Depends

from src.core.dependencies import SessionDep
from src.role.service import RoleService


def get_role_service(session: SessionDep) -> RoleService:
    """Depend Inject role service"""
    return RoleService(session)


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
