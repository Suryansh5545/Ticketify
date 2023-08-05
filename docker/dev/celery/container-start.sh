#!/bin/sh
cd /code && \
celery -A ticketify worker --loglevel=INFO
