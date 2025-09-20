# ===== Build =====
FROM maven:3.9.8-eclipse-temurin-21 AS build
WORKDIR /app

ARG GIT_REF=main
# Clone e checkout do branch/tag
RUN git clone https://github.com/RabbitDeals/rabbitdeals-api.git . \
 && git checkout ${GIT_REF}

# Build do JAR gordo, PULANDO TESTES
RUN mvn -B -DskipTests clean package spring-boot:repackage

# ===== Runtime =====
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/*-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
