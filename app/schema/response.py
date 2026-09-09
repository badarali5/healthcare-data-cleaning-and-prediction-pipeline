from typing import Any
from pydantic import BaseModel
from fastapi import status


class ResponseModel(BaseModel):
    status_code: int
    status: str
    message: str
    data: Any = None

    @classmethod
    def success(cls, message: str, data: Any = None):
        return cls(
            status_code=status.HTTP_200_OK,
            status="success",
            message=message,
            data=data
        )

    @classmethod
    def created(cls, message: str, data: Any = None):
        return cls(
            status_code=status.HTTP_201_CREATED,
            status="success",
            message=message,
            data=data
        )

    @classmethod
    def error(cls, status_code: int, message: str, data: Any = None):
        return cls(
            status_code=status_code,
            status="error",
            message=message,
            data=data
        )