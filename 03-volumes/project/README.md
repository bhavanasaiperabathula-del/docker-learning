# Notes API

A simple FastAPI Notes application where users can create and view notes.
The application is fully containerized using Docker.
Previously, data was lost whenever the container stopped or was removed.
By attaching Docker volumes, the notes are now stored persistently even after container restarts.

## Features

- Add a note (`POST /add/notes`)  
- List all notes (`GET /notes/all`)  
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
docker build -t notes-app-volume .
```

* Create a Docker volume for persistent storage
```
docker volume create notes-data
```

* Run the container with attached volume

```
docker run -d --name app-volume  -p 8000:8000 -v notes-data:/data notes-app-volume
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