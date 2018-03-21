FROM python:2.7

COPY . /
WORKDIR /

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
