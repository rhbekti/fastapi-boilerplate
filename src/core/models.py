from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class IResponse[T](BaseModel):
    """Making Global Response Format"""

    success: bool = True
    message: str = "Operation successful"
    data: T | None = None
