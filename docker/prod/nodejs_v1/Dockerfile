FROM node:18.16.0 as builder

ARG NODE_ENV
RUN npm install -g @angular/cli@16.0.4
RUN mkdir /code

# Copy codebase
COPY . /code

WORKDIR /code

ADD frontend/package.json frontend/yarn.lock /code/
RUN yarn install
ENV PATH="/code/node_modules/.bin:$PATH"

RUN ng build --configuration=${NODE_ENV}

FROM nginx:1.25.1-alpine
ARG NODE_ENV
COPY docker/prod/nodejs_v1/nginx_${NODE_ENV}.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /code/dist /usr/share/nginx/html