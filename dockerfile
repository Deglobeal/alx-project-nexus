# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . /app/

# Expose Django port
EXPOSE 8000

# Default command (overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
