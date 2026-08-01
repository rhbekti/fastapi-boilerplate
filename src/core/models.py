from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class IResponse(BaseModel, Generic[T]):
    """Making Global Response Format"""

    success: bool = True
    message: str = "Operation successful"
    data: T | None = None
