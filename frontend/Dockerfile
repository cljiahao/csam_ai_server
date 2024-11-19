# ARGs for image versions
ARG NODE=node:20.17.0-alpine3.20
ARG NGINX=nginx:alpine

# Stage 1: Base image for dependency installation
FROM $NODE AS base
WORKDIR /app
COPY ./package.json ./pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Stage 2: Build the application for staging and production
FROM base AS build-stage
COPY ./ ./
RUN pnpm run build-stage

FROM base AS build
COPY ./ ./
RUN pnpm run build

# Development image
FROM base AS dev
COPY ./ ./
CMD ["pnpm", "run", "dev"]

# Staging image
FROM base AS stage
COPY ./.env.stage ./vite.config.js ./
COPY --from=build-stage ./app/dist ./dist
CMD ["pnpm", "run", "preview-stage"]

# Production image:
FROM $NGINX AS prod
COPY --from=build ./app/dist ./usr/share/nginx/html
COPY ./nginx.conf.template ./etc/nginx/templates/nginx.conf.template
CMD ["nginx", "-g", "daemon off;"]