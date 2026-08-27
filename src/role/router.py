from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.role.dependencies import RoleServiceDep
from src.role.schemas import CreateRole, RoleResponse, UpdateRole

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=Sequence[RoleResponse])
async def find_all(
    service: RoleServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await service.find_all(offset=offset, limit=limit)


@router.post("/", response_model=RoleResponse, status_code=201)
async def create(payload: CreateRole, service: RoleServiceDep):
    return await service.create(payload)


@router.get("/{id}", response_model=RoleResponse | None)
async def find_one(id: UUID, service: RoleServiceDep):
    role = await service.find_one(id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.put("/{id}", response_model=RoleResponse | None)
async def update(id: UUID, payload: UpdateRole, service: RoleServiceDep):
    role = await service.update(id, payload)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.delete("/{id}", status_code=204)
async def remove(id: UUID, service: RoleServiceDep):
    deleted = await service.remove(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
