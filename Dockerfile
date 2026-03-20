# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Run FastAPI
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "10000"]