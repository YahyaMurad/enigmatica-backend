from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HeartbeatCreate(BaseModel):
    entity: str
    alternate_project: Optional[str] = None
    project_folder: Optional[str] = None
    project_root_count: Optional[int] = None
    language: Optional[str] = None
    time: datetime
    is_write: Optional[bool] = False
    lineno: Optional[int] = None
    cursorpos: Optional[int] = None
    lines_in_file: Optional[int] = None
    line_changes: Optional[int] = None
    is_unsaved_entity: Optional[bool] = None


class HeartbeatOut(HeartbeatCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # allows SQLAlchemy models to be returned directly
