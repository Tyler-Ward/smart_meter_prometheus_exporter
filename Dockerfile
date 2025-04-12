FROM python:3.12-alpine

ADD requirements.txt /

RUN pip install -r /requirements.txt

ADD prometheus_test.py /
ADD decoder.py /
ADD recorder.py /

CMD ["python", "/prometheus_test.py"]
