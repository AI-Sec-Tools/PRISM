# PRISM - Priority Risk Intelligence & Scoring Manager
# Production Docker Container

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r prism && useradd -r -g prism prism
RUN chown -R prism:prism /app
USER prism

# Expose port
EXPOSE 8080

# Default command
CMD ["python", "prism.py", "dashboard"]
