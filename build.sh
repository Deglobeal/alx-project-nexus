#!/bin/bash

echo "🚀 Running build.sh script..."

# Exit immediately if a command fails
set -o errexit  

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser (optional, only if you want auto-creation)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "✅ Build process completed successfully!"
