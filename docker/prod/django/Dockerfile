FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r prod.txt
ADD . /code

CMD ["sh", "/code/docker/prod/django/container-start.sh"]