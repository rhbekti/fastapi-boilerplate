from src.user.models import User, CreateUserRequest, UpdateUserRequest
from datetime import datetime
from typing import List, Optional
import uuid


class UserService:
    def __init__(self):
        # Initialize with dummy data
        self._users = [
            User(
                id="1",
                name="John Terry",
                username="john",
                email="john@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                id="2",
                name="Jane Doe",
                username="jane",
                email="jane@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            User(
                id="3",
                name="Bob Smith",
                username="bob",
                email="bob@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

    def findAll(self) -> List[User]:
        """Get all users"""
        return self._users.copy()

    def findOne(self, id: str) -> Optional[User]:
        """Find a user by ID"""
        for user in self._users:
            if user.id == id:
                return user
        return None

    def create(self, data: CreateUserRequest):
        """Create a new user"""
        new_user = User(
            id=str(uuid.uuid4()),  # Generate unique ID
            name=data.name,
            username=data.username,
            email=data.email,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._users.append(new_user)
        return new_user

    def update(self, id: str, data: UpdateUserRequest) -> Optional[User]:
        """Update an existing user"""
        user = self.findOne(id)
        if not user:
            return None

        # Update fields if provided
        if data.name is not None:
            user.name = data.name
        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            user.email = data.email

        user.updated_at = datetime.now()
        return user

    def remove(self, id: str) -> bool:
        """Remove a user by ID"""
        for i, user in enumerate(self._users):
            if user.id == id:
                self._users.pop(i)
                return True
        return False
