#!/bin/sh
python manage.py migrate --noinput  && \
python manage.py collectstatic --noinput  && \
python manage.py seed && \
uwsgi --ini /code/docker/prod/django/uwsgi.ini