# ====== build (vite) ======
FROM node:20-alpine AS build
WORKDIR /app

# Precisamos do git pra clonar
RUN apk add --no-cache git

# Clone do repositório do frontend
RUN git clone https://github.com/RabbitDeals/front-end-RabbitDeals.git . \
 && git checkout main

# Instala dependências (usa lockfile do repo se existir)
RUN npm ci || npm install

# Injeta a URL da API no build (Vite lê VITE_* em build-time)
ARG VITE_API_URL=http://localhost:8080
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# ====== runtime (nginx) ======
FROM nginx:alpine
COPY --from=build /app/dist/ /usr/share/nginx/html/
# COPY nginx.conf /etc/nginx/conf.d/default.conf  # (se você tiver um nginx.conf)
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
