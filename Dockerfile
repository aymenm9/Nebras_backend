# ---- Base Image ----
FROM docker.io/library/python:3.12-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=main.settings

# Workdir
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Django project root
WORKDIR /app/nebras

# Expose port
EXPOSE 8000

# Start worker + server
CMD sh -c "\
python manage.py migrate && \
python manage.py djangohuey & \
daphne -b 0.0.0.0 -p ${PORT:-8000} main.asgi:application \
"