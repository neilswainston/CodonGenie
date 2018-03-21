FROM python:2.7-alpine

COPY . /
WORKDIR /

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

ENTRYPOINT ["python"]
CMD ["app.py"]
