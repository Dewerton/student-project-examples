FROM python:3.8-alpine3.12
WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src .

ENTRYPOINT [ "python3", "job_launcher/main.py"]