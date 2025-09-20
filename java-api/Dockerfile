# ===== Build =====
FROM maven:3.9.8-eclipse-temurin-21 AS build
WORKDIR /app

ARG GIT_REF=main
RUN git clone https://github.com/RabbitDeals/rabbitdeals-api.git . \
    && git checkout $GIT_REF

# empacota sem rodar testes e faz o repackage executável
RUN mvn -B -DskipTests clean package spring-boot:repackage

# ===== Runtime =====
FROM eclipse-temurin:21-jre
WORKDIR /app

# copia o JAR reempacotado do Spring Boot
COPY --from=build /app/target/*-SNAPSHOT.jar /app/app.jar

EXPOSE 8080
CMD ["java", "-jar", "/app/app.jar"]
