FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /hivecore-api

RUN apk update
RUN pip3 install --upgrade pip
RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq &&\
    chmod +x /usr/bin/yq

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r /hivecore-api/requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/hivecore-api/src"

LABEL maintainer="paralepsis <der.krabbentaucher@gmail.com>"
