from pydantic import BaseModel

class Notes(BaseModel):
    title: str
    category: str
    content: str

class NotesOut(Notes):
    id: int
