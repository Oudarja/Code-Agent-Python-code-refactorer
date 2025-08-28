# Backend Dockerfile
FROM python:3.12.6-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/

WORKDIR /app/app

# Expose port
EXPOSE 8000

CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]
