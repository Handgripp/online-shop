FROM python:3.11


ENV PYTHONUNBUFFERED 1


RUN mkdir /app


WORKDIR /app

RUN pip install rq psycopg2-binary pydantic[email] python-jose fastapi-mail


COPY requirements.txt /app/


RUN pip install -r requirements.txt


COPY . /app/