# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DASH_DEBUG_MODE=False
ENV HOST=0.0.0.0
ENV PORT=8051

# Expose port 8051 for the Dash app
EXPOSE 8051

# Create non-root user for security
RUN useradd -m dashuser && chown -R dashuser:dashuser /app
USER dashuser

# Run the application
CMD ["python", "dashboard.py"]
