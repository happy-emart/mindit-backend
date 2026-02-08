FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Webkit is usually enough for scraping, or Chromium)
# Installing all for safety, but can be optimized later.
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Expose port (Koyeb usually routes to 8000 by default or configurable)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
