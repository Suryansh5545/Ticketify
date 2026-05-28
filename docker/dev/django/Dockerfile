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
RUN pip install -r dev.txt

CMD ["./docker/wait-for-it.sh", "db:5432", "--", "./docker/wait-for-it.sh", "redis:6379", "--", "sh", "/code/docker/dev/django/container-start.sh"]
