# Use Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app/

# Default command (can be overridden in docker-compose.yml)
CMD ["python", "restaurant/manage.py", "runserver", "0.0.0.0:8000"]


RUN apt-get update && apt-get install -y default-libmysqlclient-dev pkg-config
RUN pip install mysqlclient
RUN pip install django-cors-headers