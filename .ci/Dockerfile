FROM python:3.12-slim

WORKDIR /app

COPY ./TodoAPP/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./TodoAPP/ ./app

CMD CMD ["gunicorn", "TodoAPP.main:app", "--bind", "0.0.0.0:80", "--reload"]