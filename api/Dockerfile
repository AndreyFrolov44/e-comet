FROM python:3.10

WORKDIR /api

RUN apt-get -qq update

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . .

EXPOSE 8000
