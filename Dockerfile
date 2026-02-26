FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# System packages needed for building wheels and MySQL client
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn mysqlclient

# Copy backend project code
COPY backend/ ./

# Use production settings in container
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Collect static files (ignore failure in case STATIC settings are not perfect yet)
RUN python manage.py collectstatic --noinput || true

# Railway will inject PORT env var
CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
