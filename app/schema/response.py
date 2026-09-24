from typing import Any
from pydantic import BaseModel


class ResponseModel(BaseModel):
    status_code: int
    status: str
    message: str
    data: Any = None