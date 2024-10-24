ARG NODE=node:lts-alpine3.19

FROM $NODE AS base
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY ./ ./

FROM $NODE AS build
WORKDIR /app
COPY --from=base ./app ./
RUN npm run build

FROM $NODE AS prod

WORKDIR /app
COPY --from=build app/package*.json .
COPY --from=build app/build ./build
COPY --from=build app/index.js .
RUN npm ci
ARG PC_NAME
ARG NGINX_PORT
ARG FASTAPI_ROOT
ARG APP_PORT
ENV REACT_APP_API "http://$PC_NAME:$NGINX_PORT$FASTAPI_ROOT"
ENV REACT_APP_PORT $APP_PORT
EXPOSE $REACT_APP_PORT
ENTRYPOINT npx react-inject-env set && node index

FROM $NODE AS dev
WORKDIR /app
COPY --from=base ./app ./
ARG PC_NAME
ARG NGINX_PORT
ARG FASTAPI_ROOT
ARG APP_PORT
ENV REACT_APP_API "http://$PC_NAME:$NGINX_PORT$FASTAPI_ROOT"
ENV REACT_APP_PORT $APP_PORT
EXPOSE $REACT_APP_PORT
ENTRYPOINT npx react-inject-env set && npm start