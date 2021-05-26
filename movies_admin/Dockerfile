FROM python:3.9-alpine

RUN mkdir /web_django
WORKDIR /web_django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements/base.txt /web_django/
COPY requirements/production.txt /web_django/
RUN pip install -r production.txt

