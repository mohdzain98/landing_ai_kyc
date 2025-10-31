from pydantic import BaseModel
from typing import Optional, Any


class Response(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None
