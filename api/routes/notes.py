from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.models.user import UserInDB
from app.models.note import NoteCreate, Note, NoteUpdate
from app.services import note_service
from app.api.dependencies import get_current_user

router = APIRouter(tags=["notes"])

@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Create a new note for the authenticated user."""
    return await note_service.create_note(current_user.user_id, note)

@router.get("/", response_model=List[Note])
async def read_notes(current_user: UserInDB = Depends(get_current_user)):
    """Retrieve all notes belonging to the authenticated user."""
    return await note_service.get_notes(current_user.user_id)

@router.get("/{note_id}", response_model=Note)
async def read_note(
    note_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Retrieve a specific note by ID."""
    note = await note_service.get_note(note_id, current_user.user_id)
    if note:
        return note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update an existing note by ID."""
    updated_note = await note_service.update_note(note_id, current_user.user_id, note_update)
    if updated_note:
        return updated_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user: UserInDB = Depends(get_current_user)
) -> None:
    """Delete a note by ID."""
    if await note_service.delete_note(note_id, current_user.user_id):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
