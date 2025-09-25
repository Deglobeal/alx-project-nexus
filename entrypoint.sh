#!/bin/sh

echo "Waiting for database..."

# Wait until MySQL is ready
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "Database started"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
username='${DJANGO_SUPERUSER_USERNAME}'; \
email='${DJANGO_SUPERUSER_EMAIL}'; \
password='${DJANGO_SUPERUSER_PASSWORD}'; \
User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)" | python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Run Gunicorn server
gunicorn restaurant.wsgi:application --bind 0.0.0.0:8000
