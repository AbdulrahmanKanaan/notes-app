from dependencies.auth import get_current_user
from models.user import User
from pydantic.types import UUID4
from repositories.notes_repository import NotesRepository
from fastapi.params import Depends
from models.note import NoteBase
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/trusted-api', tags=['trusted-api'])


@router.get('/notes/{uuid}', response_model=NoteBase)
def show(
    uuid: UUID4,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    note = repo.getNoteByUuid(uuid)
    if (not note or user.id != note.user_id):
        raise HTTPException(status_code=404, detail="Note was not found.")
    return note
