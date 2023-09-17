FROM node:18.16.0

RUN npm install -g @angular/cli@16.0.4
RUN mkdir /code

# Copy codebase
COPY . /code

WORKDIR /code

ADD frontend/package.json frontend/yarn.lock /code/
RUN yarn install
ENV PATH="/code/node_modules/.bin:$PATH"

# Install fonts
RUN mkdir -p /usr/share/fonts/truetype/helvetica
ADD templates/fonts/* /usr/share/fonts/truetype/helvetica/
RUN fc-cache -f -v

CMD ["yarn","start", "--verbose", "--host", "0.0.0.0", "--poll", "2000"]