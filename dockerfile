FROM python:3.7-alpine3.16
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

