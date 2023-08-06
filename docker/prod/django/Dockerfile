FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

#System Dependencies
RUN apt-get update
RUN apt-get install -y wkhtmltopdf

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r dev.txt

CMD ["sh", "/code/docker/prod/django/container-start.sh"]