FROM python:3.6.6-alpine3.8

RUN apk update && apk add git
RUN apk add --no-cache libffi-dev build-base py2-pip python2-dev openssl-dev
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
RUN adduser -u 1000 -S ansible && chown -R ansible /app
