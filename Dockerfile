# Official Playwright Python image: Chromium + deps pre-installed, no ttf-unifont hell
FROM mcr.microsoft.com/playwright/python:v1.41.2-jammy

WORKDIR /app

# Copy requirements and install dependencies (uv: faster resolver, no pip backtracking hell)
COPY requirements.txt .
RUN pip install uv && \
    uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY . .

# Expose port (Koyeb usually routes to 8000 by default or configurable)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
