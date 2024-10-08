ARG NODE=node:20.17.0-alpine3.20

# Stage 1: Base image for dependency installation
FROM $NODE AS base
WORKDIR /app
COPY ./package.json ./pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY ./ ./

# Stage 2: Build the application
FROM base AS build
RUN pnpm run build

# Production image
FROM $NODE AS prod
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
CMD ["npx", "serve", "dist"]

# Staging image
FROM $NODE AS stage
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
CMD ["pnpm", "run", "stage"]

# Development image
FROM base AS dev
CMD ["pnpm", "run", "dev"]