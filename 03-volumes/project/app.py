from fastapi import FastAPI
from models.notes import notes
import json, os

app = FastAPI()

DB_FILE =  "/data/notes.json"

if not os.path.exists(DB_FILE):
   with open(DB_FILE, "w") as f:
      json.dump({}, f)

def load():
    try:
      with open(DB_FILE, 'r') as f:
         data = json.load(f)
         return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
       return {}
   
def save(data):
   with open(DB_FILE, "w") as f:
      json.dump(data, f , indent=4)

data = load()
if data:
   next_id = max(map(int, data.keys())) + 1
else:
   next_id = 1   

@app.post("/add/notes")
def add_notes(note: notes):
    global next_id
    data = load()
    data[str(next_id)] = note.dict()
    save(data)

    response_id = next_id
    next_id += 1
    return {"message": "note stored successfully", "id": response_id}

@app.get("/notes/all")
def list_notes():
    return load()
