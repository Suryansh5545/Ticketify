FROM node:18.16.0 as builder

ARG NODE_ENV
RUN npm install -g @angular/cli@16.0.4

WORKDIR /code
COPY frontend/package.json frontend/yarn.lock /code/

# Install fonts
RUN mkdir -p /usr/share/fonts/truetype/helvetica
ADD templates/fonts/* /usr/share/fonts/truetype/helvetica/
RUN fc-cache -f -v

RUN npm update
RUN yarn install
ENV PATH="/code/node_modules/.bin:$PATH" 
COPY frontend/ /code
RUN ng build --configuration=${NODE_ENV}

FROM nginx:1.25.1-alpine
ARG NODE_ENV
COPY docker/prod/nodejs_v1/nginx_${NODE_ENV}.conf /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /code/dist/ticketify /usr/share/nginx/html