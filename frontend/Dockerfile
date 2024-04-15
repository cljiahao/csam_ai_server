FROM node:lts-alpine3.19 as base
WORKDIR /app
COPY ./package*.json ./
EXPOSE 3001

FROM base as prod
ENV NODE_ENV=prod
RUN npm ci
COPY ./ ./
RUN npm run build
CMD ["node", "index"]

# Development specific setup
FROM base as dev
ENV NODE_ENV=development
RUN npm install -g nodemon && npm install
COPY ./ ./
CMD ["nodemon", "app"]