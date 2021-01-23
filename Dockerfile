FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code

RUN mkdir /data
VOLUME /data

ADD requirements.txt /code/
ADD login.txt /code/
RUN \
  apk add --no-cache libstdc++ && \
  apk add --no-cache --virtual .build-deps gcc g++ && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

ADD downloadall.py /code/
CMD python3 downloadall.py