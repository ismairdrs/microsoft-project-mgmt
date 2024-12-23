FROM python:3.11.1-slim

# System
ENV PYTHONUNBUFFERED=1

# Application
ENV APPLICATION_PATH=microsoft.api.main:app
ENV APPLICATION_PORT=8000
ENV APPLICATION_BIND=0.0.0.0

# create service directory
RUN mkdir /app && \
    chmod 0700 /app
WORKDIR /app
ADD . /app

# Update and upgrade dependencies
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
    curl \
    git \
    openssh-server \
    gcc \
    libc-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN ls /app


# Upgrade pip and install dependencies
RUN pip install --upgrade pip

RUN ls /app
RUN pip install -r /app/requirements.txt

# configurate system group
RUN addgroup --gid 999 microsoftgroup && \
    useradd --uid 999 --gid microsoftgroup microsoft

# Set permissions
RUN chown -R microsoft:microsoftgroup /app
RUN chmod 755 /app
RUN chmod +x ./infrastructure/docker/entrypoint.sh

EXPOSE 8000

USER microsoft