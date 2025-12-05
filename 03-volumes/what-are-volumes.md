# Docker Volumes – Complete Guide

## 📌 What is a Volume?

A Docker Volume is a mechanism for persistent data storage that stores data outside of a container's filesystem and is managed by Docker.

* When a container is stopped, restarted, or removed, the data stored in the volume still exists.

* When you create a volume, it's stored within a directory on the Docker host machine.

* When the volume is mounted into a container, this host directory is what gets mounted into the container's specified location.

---

## 🎯 Why Use Volumes?

Containers are **ephemeral** (short-lived).  
If data is stored inside a container → **data is lost when container is removed** ❌  
Volumes provide **persistent data** ✔

Use cases:
- Databases
- Uploaded files
- Logs
- Application state

---

## 🔹 Types of Docker Volumes

Docker supports 2 types:

1️⃣ **Named Volumes**  
2️⃣ **Anonymous (Unnamed) Volumes**

---

## 1️⃣ Named Volume

### ✔ Features

- Custom name assigned
- Easy to reuse and share
- Created explicitly

### Create Volume
```

docker volume create myVolume
docker run -d -p 8000:8000 -v myVolume:<directory> <docker_image>

```
---

### Important Behaviour
| Situation                              | What Happens                             |
| -------------------------------------- | ---------------------------------------- |
| Container has files + volume has files | Volume data **overrides** container data |
| Container has files + volume is empty  | Files **copied** from container → volume |

To prevent copy:

```

--mount volume-nocopy

```

---

## 2️⃣ Anonymous (Unnamed) Volumes

Anonymous volumes are Docker-managed volumes assigned a random unique name automatically.
They are created when a container needs persistent storage but no explicit volume name is provided.

### ✔ Features

* Docker automatically creates and manages the volume (no user-defined name)
* Persist beyond container removal unless explicitly deleted
* Each container gets its own anonymous volume if used repeatedly
* Useful to avoid overwriting data that exists inside images

### Create anonymous volume by running:
```

docker run -d --name c1 -v /data <docker_image>


```

### If we want to reuse volume between containers

#### Find Volume ID

```
docker volume ls
```

#### Reuse same anonymous volume:

```
docker run -d --name c2 -v <volume_id>:<container_directory> <docker_image>
```

---

## 📦 Mounting Volumes

Docker supports two ways to mount volumes using `docker run`:

| Syntax | Recommendation |
|--------|----------------|
| `--mount` | ⭐ Preferred — more explicit & powerful |
| `-v` / `--volume` | Older & less flexible |

---

### ✔ Using `--mount`

```bash
docker run -d \
  --mount type=volume,source=myVolume,target=/data \
  docker_image
```

---

## 🔌 When should we use `--mount`?

### 1️⃣ Specify Volume Driver Options

A **Volume Driver** tells Docker where & how data is stored.

Default → stored locally  
But can also store in:

| Storage Backend | Examples |
|----------------|----------|
| Cloud Block Storage | AWS EBS, Azure Disk, GCP Disk |
| Network File Storage | NFS, CIFS |
| Distributed Systems | Ceph, GlusterFS |
| Third-party Plugins | Portworx, Flocker |

📌 This is required in real cloud production environments

---

### 2️⃣ Mount a Subdirectory from a Volume

Example:
```bash
docker run -d \
  --mount type=volume,source=myVolume,target=/logs,volume-subpath=service1 \
  docker_image
```

---

## 🧰 --mount Options Summary

| Option | Description |
|--------|-------------|
| `source`, `src` | Volume name |
| `target`, `destination`, `dst` | Mount path inside container |
| `volume-subpath` | Mount specific subfolder |
| `readonly`, `ro` | Read-only access |
| `volume-nocopy` | Prevent auto-copy of container files into empty volume |
| `volume-opt` | Plugin/driver options |

---

## 📝 `--volume` (`-v`) Options

| Option | Description |
|--------|-------------|
| `ro` | Mount as read-only |
| `volume-nocopy` | Disable file-copy behavior |










