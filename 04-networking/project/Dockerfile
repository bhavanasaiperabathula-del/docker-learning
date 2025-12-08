FROM python:3.13-slim

# Set working directory
WORKDIR /src/app

# Install system dependencies required for psycopg2 / Postgres client
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# copy dependency list
COPY  requirements.txt .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy source code into image
COPY . .

# Create non-root user
RUN useradd -m -s /bin/bash appuser \
  && chown -R appuser:appuser /src/app
    
#switch to non-root user
USER appuser

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

