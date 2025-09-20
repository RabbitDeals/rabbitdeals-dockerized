FROM node:20-alpine AS build
WORKDIR /app

RUN apk add --no-cache git

ARG FRONTEND_GIT_REF=main

RUN git clone https://github.com/RabbitDeals/front-end-RabbitDeals.git .
RUN git checkout $FRONTEND_GIT_REF

RUN npm ci
ENV VITE_API_URL=/api
RUN npm run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/html

COPY --from=build /app/dist/ ./

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
