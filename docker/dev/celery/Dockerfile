FROM python:3.11

#System Dependencies
RUN apt-get update
RUN apt-get install -y wkhtmltopdf

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r dev.txt

CMD ["sh", "/code/docker/dev/celery/container-start.sh"]