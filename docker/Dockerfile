FROM python:3.12-slim

WORKDIR /app

RUN apt-get update & apt-get install -y git

RUN git clone https://github.com/geopython/pygeoapi.git ~

RUN pip install -e ~/pygeoapi


