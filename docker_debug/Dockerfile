FROM python:3.7.0-alpine3.8

EXPOSE 5000 5000
ENV FLASK_APP /app/server.py
CMD python -m flask run --host 0.0.0.0
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
USER 1000
COPY templates templates
COPY server.py server.py
COPY helloworld.txt helloworld.txt
COPY static static
COPY colour.py colour.py
