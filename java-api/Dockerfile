# Fase de build
FROM maven:3.9.8-eclipse-temurin-21 AS build

WORKDIR /app

# Argumento de referência do Git para escolher o branch
ARG GIT_REF=main

# Clonando o repositório e trocando para o branch especificado
RUN git clone https://github.com/RabbitDeals/rabbitdeals-api.git . \
    && git checkout $GIT_REF

# Construindo o projeto Maven
RUN mvn -B -DskipTests clean package

# Fase de runtime (apenas o JRE)
FROM eclipse-temurin:21-jre

WORKDIR /app

# Copiando o JAR do build anterior
COPY --from=build /app/target/*.jar app.jar

# Expondo a porta 8080
EXPOSE 8080

# Rodando a aplicação
CMD ["java", "-jar", "app.jar"]
