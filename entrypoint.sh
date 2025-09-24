#!/bin/sh

# Exit immediately if a command fails
set -e

# Apply database migrations
echo "Applying database migrations..."
python restaurant/manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python restaurant/manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
import os
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

# Start server
echo "Starting server..."
exec "$@"
