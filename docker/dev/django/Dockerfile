FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

#System Dependencies
RUN apt-get update
RUN apt-get install -y wkhtmltopdf

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r dev.txt

# Install fonts
RUN mkdir -p /usr/share/fonts/truetype/helvetica
ADD templates/fonts/* /usr/share/fonts/truetype/helvetica/
RUN fc-cache -f -v

CMD ["./docker/wait-for-it.sh", "db:5432", "--", "./docker/wait-for-it.sh", "redis:6379", "--", "sh", "/code/docker/dev/django/container-start.sh"]
