# Python Base Image
FROM python:3.9-slim

# Python Buffer Outout Is Straight To Terminal And Set Django Settings Module
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE: config.settings

# Base Image Cleanup and Update
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and Set Working Dir
WORKDIR /recipe-api

# Copy Full Dir 
COPY . /recipe-api/

# Install All Required Packages
RUN pip install --no-cache-dir -r requirements.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Update Execute Permission for entrypoint.sh
RUN chmod +x /recipe-api/entrypoint.sh
RUN chown root:root /recipe-api/entrypoint.sh

# Exposing TO PORT 8000
EXPOSE 8000

# Use the entrypoint script
CMD ["/recipe-api/entrypoint.sh"]

USER django-user