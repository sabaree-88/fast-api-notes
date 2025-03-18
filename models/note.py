from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    note_title: str
    note_content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class Note(NoteBase):
    note_id: str
    user_id: str
    created_on: datetime
    last_update: datetime

    model_config = ConfigDict(
        from_attributes=True,  # ✅ Replaces 'orm_mode'
        json_schema_extra={    # ✅ Replaces 'schema_extra'
            "example": {
                "note_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "note_title": "Meeting Notes",
                "note_content": "Discussed project timeline and goals",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "created_on": "2023-01-01T00:00:00",
                "last_update": "2023-01-01T00:00:00"
            }
        }
    )
