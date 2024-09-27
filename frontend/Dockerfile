ARG NODE=node:20.17.0-alpine3.20

# Stage 1: Base image for dependency installation
FROM $NODE as base
WORKDIR /app
COPY ./package.json ./pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY ./ ./

# Stage 2: Build the application
FROM $NODE as build
WORKDIR /app
COPY --from=base ./app ./
RUN pnpm run build

# Production image
FROM $NODE as prod
WORKDIR /app
COPY --from=build /app/package.json /app/pnpm-lock.yaml ./
COPY --from=build /app/dist ./dist
COPY --from=build app/index.js .
RUN npm install -g pnpm && pnpm install --prod
ARG PC_NAME
ARG NGINX_PORT
ARG FASTAPI_ROOT
ARG APP_PORT
ENV REACT_APP_API "http://$PC_NAME:$NGINX_PORT$FASTAPI_ROOT"
ENV REACT_APP_PORT $APP_PORT
EXPOSE $REACT_APP_PORT
ENTRYPOINT npx react-inject-env set && node index

# Development image
FROM $NODE as dev
WORKDIR /app
COPY --from=base ./app ./
ARG PC_NAME
ARG NGINX_PORT
ARG FASTAPI_ROOT
ARG APP_PORT
ENV REACT_APP_API "http://$PC_NAME:$NGINX_PORT$FASTAPI_ROOT"
ENV REACT_APP_PORT $APP_PORT
EXPOSE $REACT_APP_PORT
ENTRYPOINT npx react-inject-env set && pnpm run dev