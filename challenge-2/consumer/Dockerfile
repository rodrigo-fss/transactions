FROM python:3.7-slim

WORKDIR /app

COPY consumer/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./consumer /app