from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.core.exceptions import AlreadyExistsError
from src.user.dependencies import UserServiceDep
from src.user.schemas import CreateUser, UpdateUser, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Sequence[UserResponse])
async def find_all(
    service: UserServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await service.find_all(offset=offset, limit=limit)


@router.post("/", response_model=UserResponse, status_code=201)
async def create(payload: CreateUser, service: UserServiceDep):
    try:
        return await service.create(payload)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{id}", response_model=UserResponse | None)
async def find_one(id: UUID, service: UserServiceDep):
    user = await service.find_one(id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{id}", response_model=UserResponse | None)
async def update(id: UUID, payload: UpdateUser, service: UserServiceDep):
    user = await service.update(id, payload)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{id}", status_code=204)
async def remove(id: UUID, service: UserServiceDep):
    deleted = await service.remove(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
