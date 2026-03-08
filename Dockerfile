# ---- Base Image ----
FROM docker.io/library/python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=main.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including db.sqlite3)
COPY . .

# Set working directory to the Django project root
WORKDIR /app/nebras

# Expose port
EXPOSE 8000

# Run using Daphne (ASGI server) — uses $PORT from Render, falls back to 8000 locally
CMD daphne -b 0.0.0.0 -p ${PORT:-8000} main.asgi:application
