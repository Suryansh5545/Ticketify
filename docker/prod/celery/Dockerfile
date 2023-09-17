FROM python:3.11

#System Dependencies
RUN apt-get update
RUN apt-get install -y wkhtmltopdf

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
ADD requirements/* /code/
RUN pip install -r prod.txt
ADD . /code

# Install fonts
RUN mkdir -p /usr/share/fonts/truetype/helvetica
ADD templates/fonts/* /usr/share/fonts/truetype/helvetica/
RUN fc-cache -f -v

CMD ["sh", "/code/docker/prod/celery/container-start.sh"]
