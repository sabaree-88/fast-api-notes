from datetime import datetime
import uuid
from typing import List, Optional

from app.core.db import notes_collection
from app.models.note import NoteCreate, NoteUpdate, Note

async def create_note(user_id: str, note: NoteCreate) -> Note:
    note_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    note_data = Note(
        note_id=note_id,
        user_id=user_id,
        note_title=note.note_title,
        note_content=note.note_content,
        created_on=now,
        last_update=now
    )
    
    await notes_collection.insert_one(note_data.dict())
    return note_data

async def get_notes(user_id: str) -> List[Note]:
    notes = []
    cursor = notes_collection.find({"user_id": user_id})
    async for note in cursor:
        notes.append(Note(**note))
    return notes

async def get_note(note_id: str, user_id: str) -> Optional[Note]:
    if note := await notes_collection.find_one({"note_id": note_id, "user_id": user_id}):
        return Note(**note)
    return None

async def update_note(note_id: str, user_id: str, note_update: NoteUpdate) -> Optional[Note]:
    now = datetime.utcnow()
    
    # Verify note exists and belongs to user
    if not await get_note(note_id, user_id):
        return None
    
    update_data = {
        "note_title": note_update.note_title,
        "note_content": note_update.note_content,
        "last_update": now
    }
    
    await notes_collection.update_one(
        {"note_id": note_id, "user_id": user_id},
        {"$set": update_data}
    )
    
    updated_note = await notes_collection.find_one({"note_id": note_id})
    return Note(**updated_note)

async def delete_note(note_id: str, user_id: str) -> bool:
    # Verify note exists and belongs to user
    if not await get_note(note_id, user_id):
        return False
    
    result = await notes_collection.delete_one({"note_id": note_id, "user_id": user_id})
    return result.deleted_count > 0