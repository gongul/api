FROM pypy:3.8-slim-buster

LABEL "maintainer"="gongul <projectgongul@gmail.com>"

RUN apt-get update && apt-get install -y \
    python-dev libc6 python-greenlet-dev \
    dpkg-dev


WORKDIR /ably/ably-api

ADD docker-requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD . ./

WORKDIR /ably/ably-api/src

CMD ["gunicorn","common.wsgi.local:application","--max-requests","1000","-k","gevent","--max-requests-jitter","60","--bind","0.0.0.0:3000"]


