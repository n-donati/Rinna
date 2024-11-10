# Use the official Python 3.12 image from Docker Hub
FROM python:3.12-slim

# Set environment variables to avoid any input prompts during installation
ENV PYTHONUNBUFFERED=1
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true

# Install necessary system packages, including libssl and ICU for OpenSSL support
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libicu-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose the port Railway will use
EXPOSE 8000

# Run migrations and start Django using Gunicorn
RUN python manage.py makemigrations app
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "rinna.wsgi:application", "--bind", "0.0.0.0:8000"]
