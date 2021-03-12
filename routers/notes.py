from dependencies.auth import get_current_user
from models.user import User
from typing import List
from models.note import Note, NoteColor, NoteCreate
from fastapi.params import Depends
from repositories.notes_repository import NotesRepository
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('/', response_model=List[Note])
def index(repo: NotesRepository = Depends(NotesRepository), user: User = Depends(get_current_user)):
    notes = repo.getNotes(userId=user.id)
    return notes


@router.post('/', response_model=Note)
def store(
    note: NoteCreate,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    created_note_id = repo.createNote(note, user.id)
    created_note = repo.getNoteById(created_note_id)
    if (created_note):
        return created_note
    raise HTTPException(
        status_code=400, detail="Something went wrong!, note was not created."
    )


@router.get('/{note_id}', response_model=Note)
def show(
    note_id: int,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    note = repo.getNoteById(note_id)
    if (not note or user.id != note.user_id):
        raise HTTPException(status_code=404, detail="Note was not found.")
    return note


@router.put('/{note_id}', response_model=Note)
def update(
    note_id: int,
    note: NoteCreate,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    mynote = repo.getNoteById(note_id)
    if (not mynote or user.id != mynote.user_id):
        raise HTTPException(status_code=404, detail="Note was not found.")
    mynote = repo.updateNote(note_id, note)
    mynote = repo.getNoteById(note_id)
    return mynote


@router.delete('/{note_id}', response_model=Note)
def delete(
    note_id: int,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    mynote = repo.getNoteById(note_id)
    if (not mynote or user.id != mynote.user_id):
        raise HTTPException(status_code=404, detail="Note was not found.")
    repo.trashNote(note_id)
    return mynote


@router.put('/{note_id}/change-color', response_model=Note)
def update_color(
    note_id: int,
    noteColor: NoteColor,
    repo: NotesRepository = Depends(NotesRepository),
    user: User = Depends(get_current_user)
):
    mynote = repo.getNoteById(note_id)
    if (not mynote or user.id != mynote.user_id):
        raise HTTPException(status_code=404, detail="Note was not found.")
    mynote = repo.changeNoteColor(note_id, noteColor.color.value)
    mynote = repo.getNoteById(note_id)
    return mynote
