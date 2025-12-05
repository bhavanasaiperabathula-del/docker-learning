# Notes API

A simple **FastAPI** project to manage notes.  
Users can **add, list, get by ID, and delete notes**.  
The project is **containerized with Docker** for easy setup and deployment.

## Features

- Add a note (`POST /add/notes`)  
- List all notes (`GET /notes/all`)  
- Get note by ID (`GET /notes/{id}`)  
- Delete note by ID (`DELETE /notes/{id}`)  
- Runs in a Docker container for consistency  
- Lightweight and easy to extend

---

## Tech Stack

- **Python 3.13**  
- **FastAPI** (API framework)  
- **Uvicorn** (ASGI server)  
- **Docker** (containerization)

---

## Clone the repository

```
git clone <repo-url>
cd project
```

---

## Running with Docker
* Build Docker image

```
docker build -t notes-app .
```

* Run the container

```
docker run -p 8000:8000 notes-app
```

---

## API Endpoints

| Method | Endpoint      | Description                                                                |
| ------ | ------------- | ---------------------------------------------------------------------------|
| POST   | `/add/notes`  | Add a new note. Body: `{ "title": "Docker learning", "category": "Devops", "content" :  Understanding images, containers, and volumes"] }`                                                                  |
| GET    | `/notes/all`  | Get all notes                                                              |
                                                

---


## Access the API

* FastAPI docs (Swagger UI): http://localhost:8000/docs