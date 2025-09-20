# Fase de build para o frontend
FROM node:20-alpine AS build

WORKDIR /app

# Instalando git para clonar o repositório
RUN apk add --no-cache git

# Argumento de referência do Git para escolher o branch
ARG FRONTEND_GIT_REF=main

# Clonando o repositório e trocando para o branch especificado
RUN git clone https://github.com/RabbitDeals/front-end-RabbitDeals.git . \
    && git checkout $FRONTEND_GIT_REF

# Instalando dependências do frontend
RUN npm ci

# Definindo a URL da API para o frontend
ENV VITE_API_URL=/api

# Rodando o build do frontend
RUN npm run build

# Fase de produção com Nginx
FROM nginx:alpine

# Definindo diretório do Nginx
WORKDIR /usr/share/nginx/html

# Copiando os arquivos gerados pelo build para o diretório do Nginx
COPY --from=build /app/dist/ ./

# Copiando a configuração personalizada do Nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expondo a porta 80
EXPOSE 80
