from fastapi import FastAPI,  Depends
from dto.notes import Notes, NotesOut
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models_db.notes_db import Note, Base
import json, os
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()

# Create tables if they don't exist
@app.on_event("startup")
def on_startup():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB is ready")
            break
        except OperationalError:
            print("DB not ready yet, retrying...")
            time.sleep(2)
    else:
        print("DB never became ready")
        raise


# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add/notes")
def add_notes(note: Notes, db: Session = Depends(get_db)):
    db_note = Note(
        title=note.title,
        category=note.category,
        content=note.content,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)  # gets the auto-generated ID

    return {
        "message": "note stored successfully",
        "id": db_note.id,
    }


@app.get("/notes/all")
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "category": n.category,
            "content": n.content,
        }
        for n in notes
    ]
