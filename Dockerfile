FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY TodoAPP/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY TodoAPP/ .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60"]