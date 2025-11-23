# 🐳 Dockerfile — Explanation, Purpose & Examples

# 📌 What is a Dockerfile?

## A Dockerfile:

* 📝 Is a text-based, read-only template that defines how to build an image
* 🧱 Builds the environment needed to run your application
* 🧩 Creates a layer for each instruction
* 🚀 Uses caching to speed up future builds
* 📦 Produces a Docker image at the end

---

# 🧱 How Docker Layers Work

* Every instruction (FROM, COPY, RUN, etc.) creates a new immutable layer.
* Docker caches these layers.
* When you rebuild:
  * If a layer has not changed, Docker reuses the cache.
  * If a layer changes, Docker rebuilds that layer + everything after it.

---

# ⚡ Why Caching is Useful

* Only rebuilds changed layers → much faster builds
* Avoid re-installing Python, system tools, or dependencies
* Saves CPU, disk space, and time

---

# 📁 Example Dockerfile (With Explanation)

```
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## ▶️ **Layer-by-Layer Explanation**

* FROM python:3.12-slim 
    Downloads the base Python image (small, minimal version).

* WORKDIR /app
    Sets the working directory inside the container.

* COPY requirements.txt .
    Copies only the dependency file.

* RUN pip install -r requirements.txt
    Installs Python libraries (cached unless requirements.txt changes).

* COPY . .
    Copies the rest of your project code.

* CMD ["python", "main.py"]
    The command that runs when the container starts.

## 🔄 **Caching Effect**

* Steps 1–4 rarely change → Docker reuses cache
* Step 5 changes often (your code) → only this layer is rebuilt

---

# 🧰 Dockerfile Instructions Explained

## 🧱 **FROM**

* Downloads the base image

```
FROM python:3.12-slim
```

* The tag (e.g., slim) defines the image variant (lighter → fewer tools)

---

## 📂 **WORKDIR**

* Sets the directory where commands will run inside the container

```
WORKDIR /app
```
---

## 📥 **COPY**

* Copies files from host → container

```
COPY requirements.txt .
```
---

## 🛠 **RUN**

* Executes commands while building the image

```
RUN pip install -r requirements.txt
```

* Used for:
  * Installing packages
  * Creating directories
  * Configuring environment

---

## 🚀 **CMD**

* Runs when container starts
* Only one CMD is allowed

```
CMD ["python", "main.py"]
```

---

# 🔧 Extra Commands You Should Know

## 📦 **ADD**

* Everything COPY does plus:
  * Can extract .tar.gz files automatically
  * Can download files from URL

⚠ Recommendation:
👉 Prefer COPY unless you specifically need ADD’s extra features.

---

## 🏁 **ENTRYPOINT**

* Defines a fixed command that always runs.
* CMD can provide default arguments.

```
ENTRYPOINT ["sleep"]
CMD ["10"]
```

* Default: sleep 10
* Override: docker run myimage 5
→ sleep 5

---

## 🌍 **ENV**

* Used to declare environment variables.

```
ENV PORT=8000
```

---

## ⚙️ **ARG**

* Build-time variables (available only while building the image).

```
ARG VERSION=1.0
```

---

## 🔓 **EXPOSE**

* It is a declarative instruction that tells Docker which port the application inside the container listens on.

```
EXPOSE 8000
```

* It does NOT make the port accessible externally
* To access it externally, you still need: docker run -p 8000:8000 myimage

---

## 👤 **USER**

* Specifies which user the container should run as.
* Improves security by avoiding the `root` user.

```
RUN useradd -m -s /bin/bash appuser
USER appuser
```

✅ Benefits:

- Prevents accidental system-level access  
- More secure

---

# 📝 Summary

## 🎯 Dockerfile Key Points

* **Dockerfile** = recipe for building images
* **Each instruction** = cached layer
* **Caching** → faster rebuilds
* **COPY** > **ADD** (most of the time)
* **RUN** = build time
* **CMD** = container start time
* **ENTRYPOINT** = strong command
* **WORKDIR** = project directory

## 🎯 Best Practices

* Use small base images (slim / alpine)
* Place dependencies before copying code for caching
* Use .dockerignore to avoid unnecessary files