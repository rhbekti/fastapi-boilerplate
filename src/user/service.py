from src.user.models import User, CreateUserRequest, UpdateUserRequest
from datetime import datetime
from typing import Sequence, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import UTC
import bcrypt
from src.core.exceptions import AlreadyExistsError


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        truncated = password.encode("utf-8")[:72]
        return bcrypt.hashpw(truncated, bcrypt.gensalt()).decode("utf-8")

    async def find_all(self, offset: int = 0, limit: int = 20) -> Sequence[User]:
        """Get all users"""
        result = await self.session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()

    async def find_one(self, user_id: uuid.UUID) -> Optional[User]:
        """Find a user by ID"""
        return await self.session.get(User, user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CreateUserRequest):
        """Create a new user"""
        existing = await self.get_user_by_username(data.username)

        if existing is not None:
            message = f"User already exists."
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

    async def update(
        self, user_id: uuid.UUID, data: UpdateUserRequest
    ) -> Optional[User]:
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
