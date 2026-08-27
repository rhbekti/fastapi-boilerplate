import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.core.exceptions import AlreadyExistsError
from src.user.models import User
from src.user.schemas import CreateUser, UpdateUser


class UserService:
    """User Service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        truncated = password.encode("utf-8")[:72]
        return bcrypt.hashpw(truncated, bcrypt.gensalt()).decode("utf-8")

    async def find_all(self, offset: int = 0, limit: int = 20) -> Sequence[User]:
        """Get all users"""
        result = await self.session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()  # type: ignore

    async def find_one(self, user_id: uuid.UUID) -> User | None:
        """Find a user by ID"""
        return await self.session.get(User, user_id)  # type: ignore

    async def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username"""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CreateUser):
        """Create a new user"""
        existing = await self.get_user_by_username(data.username)

        if existing is not None:
            message = "User already exists."
            raise AlreadyExistsError(message)

        hashed_password = self._hash_password(data.password)

        user = User(
            **data.model_dump(exclude={"password"}),
            password=hashed_password,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: uuid.UUID, data: UpdateUser) -> User | None:
        """Update an existing user"""
        user = await self.session.get(User, user_id)
        if not user:
            return None

        if data.password:
            hashed_password = self._hash_password(data.password)
            data.password = hashed_password

        updates = data.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(user, key, value)

        user.updated_at = datetime.now(UTC)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def remove(self, user_id: uuid.UUID) -> bool:
        """Remove a user by ID"""
        user = await self.session.get(User, user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True
