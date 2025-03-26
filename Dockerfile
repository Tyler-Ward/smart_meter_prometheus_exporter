FROM python:3.7-alpine

ADD requirements.txt /

RUN pip install -r /requirements.txt

ADD prometheus_test.py /
ADD decoder.py /

CMD ["python", "/prometheus_test.py"]
