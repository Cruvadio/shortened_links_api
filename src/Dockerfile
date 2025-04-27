# pull official base image
FROM python:3.12-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy requirements file


# install dependencies
RUN set -eux
RUN apk add --no-cache --virtual .build-deps build-base \
     libffi-dev gcc musl-dev python3-dev

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /usr/src/app/

# copy project
