# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., SQLite)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlite3 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file to the container and install Python dependencies
COPY requirements.txt /app/
COPY entrypoint.sh /usr/bin/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project into the container
COPY ./inventory-reservation-manager /app/

# Expose the port the app will run on
EXPOSE 80


ARG IMAGES_DIR=/uploads

# Set environment variables for the app (can be overridden when running the container)
ENV DEBUG=False
ENV ALLOWED_HOSTS=*
ENV DJANGO_USERNAME=Admin
ENV DJANGO_PASSWORD=irm-admin
ENV DJANGO_EMAIL=default@email.com
ENV DATABASE_DIR=/app
ENV IMAGES_DIR=${IMAGES_DIR}
ENV CSRF_TRUSTED_ORIGINS="localhost:80,127.0.0.1:80"

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

COPY ./static ${IMAGES_DIR}/static/

RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

# Entry point to run migrations and start Django server with custom configurations
CMD sh -c " \
    # Ensure DATABASE_DIR exists \
    mkdir -p \"$DATABASE_DIR\" && \
    chmod -R 755 \"$DATABASE_DIR\" && \
    mkdir -p \"$IMAGES_DIR\" && \
    chmod -R 755 \"$IMAGES_DIR\" && \
    # Make database migrations \
    python manage.py makemigrations database frontend && \
    # Run database migrations \
    python manage.py migrate && \
    # Create superuser if username and password are passed as environment variables \
    if [ -n \"$DJANGO_USERNAME\" ] && [ -n \"$DJANGO_PASSWORD\" ]; then \
        python manage.py create_custom_superuser \"$DJANGO_USERNAME\" \"$DJANGO_EMAIL\" \"$DJANGO_PASSWORD\"; \
    fi && \
    # Start Django development server with custom port and settings \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:8000 server.wsgi:application & \
    # Start Nginx to serve static/media files and act as a reverse proxy \
    nginx -g 'daemon off;'"

