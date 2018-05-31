FROM python:3.6.5-stretch

WORKDIR /srv/www

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --upgrade pip

CMD tail -f /dev/null
