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