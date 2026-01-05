FROM python:3.10-slim

WORKDIR /app

# 1. Install system dependencies needed to build mysqlclient[citation:1][citation:9]
RUN apt-get update && \
    apt-get install -y pkg-config default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# 2. Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application code
COPY . .

# The command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "main:app"]