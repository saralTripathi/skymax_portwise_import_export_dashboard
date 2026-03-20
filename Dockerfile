FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "python3 pipeline/run_pipeline.py && uvicorn api.app:app --host 0.0.0.0 --port 10000"]