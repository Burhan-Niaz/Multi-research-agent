Multi-Research-Agent
first create python file and integrate them
use streamlit and build webuserinterface 
first run on docker to check validity
place it on github and deploy by streamlit
remove api's on github and place in streamlit while advance settings
choose a name and deploy it

for docker to build first create a Dockerfile and dockerignore file and docker-compose.yml for that it will run even vs code is off
then in docker place code

.yml file code:
services:
  research-app:
    build: .
    container_name: research-system
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: always


    Dockerfile code:
    FROM python:3.11-slim

WORKDIR /app

# 1. System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Core Build Tools (Install these first to avoid pyforest errors)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Install Requirements
# Adding a longer timeout to prevent the EOF error during slow downloads
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# 4. Copy Code
COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


then run this command to build
docker compose up 
that's it


