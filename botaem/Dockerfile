FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /myapp

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

RUN python manage.py makemigrations

RUN python manage.py collectstatic --noinput

RUN python manage.py createcachetable
