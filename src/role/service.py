from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.role.models import Role
from src.role.schemas import CreateRole, UpdateRole


class RoleService:
    """Role Service"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all(self, offset: int = 0, limit: int = 20):
        """Get all roles"""
        result = await self.session.execute(select(Role).offset(offset).limit(limit))
        return result.scalars().all()

    async def find_one(self, role_id: UUID) -> Role | None:
        """Find a role by ID"""
        return await self.session.get(Role, role_id)

    async def create(self, data: CreateRole) -> Role:
        """Create a new role"""
        role = Role(**data.model_dump())

        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)

        return role

    async def update(self, role_id: UUID, data: UpdateRole) -> Role | None:
        """Update role"""
        role = await self.session.get(Role, role_id)

        if not role:
            return None

        updates = data.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(role, key, value)
        role.updated_at = datetime.now(UTC)

        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        return role

    async def remove(self, role_id: UUID) -> bool:
        role = await self.session.get(Role, role_id)

        if not role:
            return False

        await self.session.delete(role)
        await self.session.commit()
        return True
