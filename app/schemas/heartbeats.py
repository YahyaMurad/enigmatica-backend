from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HeartbeatCreate(BaseModel):
    entity: str
    type: Optional[str] = None
    category: Optional[str] = None
    project: Optional[str] = None
    branch: Optional[str] = None
    language: Optional[str] = None
    time: datetime
    is_write: Optional[bool] = False


class HeartbeatOut(HeartbeatCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # allows SQLAlchemy models to be returned directly
