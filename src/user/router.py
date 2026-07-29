from fastapi import APIRouter
from typing import List, Optional
from src.user.models import User, CreateUserRequest, UpdateUserRequest
from src.user.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
async def find_all(service: UserServiceDep) -> List[User]:
    return service.findAll()


@router.post("/")
async def create(payload: CreateUserRequest, service: UserServiceDep) -> User:
    return service.create(payload)


@router.patch("/{id}")
async def update(
    id: str, paylod: UpdateUserRequest, service: UserServiceDep
) -> Optional[User]:
    return service.update(id, paylod)


@router.delete("/{id}")
async def remove(id: str, service: UserServiceDep):
    return service.remove(id)
