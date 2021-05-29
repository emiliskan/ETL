FROM python:3.9-alpine

RUN mkdir /etl
WORKDIR /etl

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and curl
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk --no-cache add curl

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /etl/
RUN pip install -r requirements.txt

COPY wait_to_start.sh /etl/

