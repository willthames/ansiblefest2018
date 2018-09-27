FROM python:3.6.6-alpine3.8

RUN apk update && apk add git
RUN apk add --no-cache libffi-dev build-base py2-pip python2-dev openssl-dev
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
