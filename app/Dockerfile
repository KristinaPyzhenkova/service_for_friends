FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y netcat