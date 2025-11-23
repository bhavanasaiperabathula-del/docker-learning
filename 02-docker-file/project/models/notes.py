from pydantic import BaseModel

class notes(BaseModel):
    title: str
    category: str
    content: str
