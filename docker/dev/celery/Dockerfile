FROM python:3.11-bullseye


RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r dev.txt

CMD ["sh", "/code/docker/dev/celery/container-start.sh"]