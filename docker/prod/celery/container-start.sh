#!/bin/sh
cd /code && \
celery -A ticketify worker --beat --loglevel=INFO