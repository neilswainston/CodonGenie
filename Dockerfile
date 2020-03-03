FROM python:3.7

COPY . /
WORKDIR /

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
