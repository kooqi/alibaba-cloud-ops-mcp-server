# Use official Python 3.10 image as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Update package manager and install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Set port parameter, default value is 8000
ARG PORT=8000
ENV PORT=${PORT}

# Expose port
EXPOSE ${PORT}

# Set default startup command
CMD ["uvx", "alibaba-cloud-ops-mcp-server@0.9,1"]