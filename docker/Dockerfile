FROM python:3.11

WORKDIR /project

COPY ../requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .. .

ENV PYTHONPATH /project/app

CMD gunicorn --workers 4 --threads 4 settings.wsgi --timeout 36000 --max-requests 10000 -b 0.0.0.0:8000