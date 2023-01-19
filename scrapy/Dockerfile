FROM python:3.10

WORKDIR /scrapy

RUN apt-get -qq update

COPY ./requirements.txt ./scrapy/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./scrapy/requirements.txt

COPY . .

CMD [ "python3", "./run.py" ]