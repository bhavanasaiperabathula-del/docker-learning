from fastapi import FastAPI
from models.notes import notes

app = FastAPI()

notes_db = {}
next_id = 1

@app.post("/add/notes")
def add_notes(note: notes):
    global next_id
    note_data = note.dict()
    notes_db[next_id] = note_data
    next_id += 1
    return {"message": "note stored successfully", "id": next_id - 1}

@app.get("/notes/all")
def list_notes():
    return list(notes_db.values())

@app.get("/notes/{id}")
def get_notes_by_id(id: int):
    #notes_db[id] # KeyError if "content" not in dict
    note = notes_db.get(id)
    if note:
        return {"id": id, **note}
    return {"message": f"note with id {id} not found"}   

@app.delete("/notes/{id}")
def delete_by_id(id : int):
   deleted =notes_db.pop(id, None)
   if deleted:
    return {"message": f"note with id {id} deleted"}
   return {"message": f"note with id {id} not found"} 
