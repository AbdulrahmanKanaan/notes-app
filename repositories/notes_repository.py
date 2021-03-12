import uuid
from sqlalchemy.sql.expression import text
from models.note import Note, NoteCreate
from typing import List
from .repository import Repository


class NotesRepository(Repository):

    def __init__(self) -> None:
        super().__init__()

    def getNoteById(self, id: int, withTrashed=False) -> Note:
        stmt = text(
            "SELECT * FROM notes WHERE id=:id AND deleted_at IS " +
            ("NOT NULL" if withTrashed else "NULL")
        )
        result = self.db.execute(stmt, id=id).fetchone()
        if (result):
            return Note(**result)
        return None

    def getNoteByUuid(self, uuid: str, withTrashed=False) -> Note:
        trashed = "" if withTrashed else " AND deleted_at IS NULL"
        stmt = text(
            "SELECT * FROM notes WHERE uuid=:uuid" + trashed
        )
        result = self.db.execute(stmt, uuid=uuid).fetchone()
        if (result):
            return Note(**result)
        return None

    def getNotes(self, userId: int, withTrashed=False) -> List[Note]:
        trashed = "" if withTrashed else " AND deleted_at IS NULL"
        stmt = text(
            "SELECT * FROM notes WHERE user_id=:user_id" + trashed
        )
        result = self.db.execute(stmt, user_id=userId).fetchall()
        notes = []
        for row in result:
            notes.append(Note(**row))
        return notes

    def createNote(self, note: NoteCreate, userId: int) -> int:
        stmt = text(
            "INSERT INTO notes(uuid, title, content, user_id, created_at, updated_at)" +
            "VALUES(:uuid, :title, :content, :user_id, NOW(), NOW())"
        )
        result = self.db.execute(
            stmt, uuid=str(uuid.uuid4()),
            title=note.title, content=note.content,
            user_id=userId,
        )
        return result.lastrowid

    def updateNote(self, id: int, note: NoteCreate) -> None:
        stmt = text(
            "UPDATE notes SET title = :title, content = :content, updated_at = NOW() WHERE id = :id"
        )
        self.db.execute(
            stmt,
            title=note.title, content=note.content, id=id
        )
        return

    def trashNote(self, id: int) -> None:
        stmt = text(
            "UPDATE notes SET deleted_at = NOW() WHERE id = :id"
        )
        self.db.execute(stmt, id=id)
        return

    def deleteNote(self, id: int) -> None:
        stmt = text(
            "DELETE FROM notes WHERE id = :id"
        )
        self.db.execute(stmt, id=id)
        return

    def changeNoteColor(self, id: int, color: str) -> None:
        print(color)
        stmt = text(
            "UPDATE notes SET color = :color, updated_at = NOW() WHERE id = :id"
        )
        self.db.execute(stmt, color=color, id=id)
        return
