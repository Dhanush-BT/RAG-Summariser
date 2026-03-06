# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Set workdir
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpoppler-cpp-dev \
        poppler-utils \
        git \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if you plan to run API later
EXPOSE 5000

# Default command (interactive RAG)
CMD ["python", "rag.py"]