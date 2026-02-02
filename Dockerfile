# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies and tkinter
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# Expose the default port
EXPOSE 8080

# CMD to start the app
CMD ["python", "main.py"]
