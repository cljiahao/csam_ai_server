ARG NODE=node:20.17.0-alpine3.20

# Stage 1: Base image for dependency installation
FROM $NODE as base
WORKDIR /app
COPY ./package.json ./pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY ./ ./

# Stage 2: Build the application
FROM base as build
RUN pnpm run build

# Production image
FROM $NODE as prod
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/pnpm-lock.yaml ./
RUN pnpm install --prod --frozen-lockfile
CMD ["npx", "serve", "dist"]

# Development image
FROM base as dev
CMD ["pnpm", "run", "dev"]