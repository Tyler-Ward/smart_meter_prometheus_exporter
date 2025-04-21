FROM python:3.12-alpine

ADD requirements.txt /

RUN pip install -r /requirements.txt

ADD prometheus_exporter.py /
ADD decoder.py /
ADD recorder.py /

CMD ["python", "/prometheus_exporter.py"]
