from pydantic.types import UUID4
from constants.colors import Colors
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteColor(BaseModel):
    color: Optional[Colors] = None

class NoteBase(NoteCreate, NoteColor):
    pass

class Note(NoteBase):
    id: int
    uuid: UUID4
    user_id: int
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
