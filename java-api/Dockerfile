# =======================
# STAGE 1: BUILD
# =======================
FROM maven:3.9.8-eclipse-temurin-21 AS build

WORKDIR /app

# Copiamos só o pom primeiro para aproveitar cache de dependências
COPY pom.xml .

# Baixa dependências (sem compilar ainda)
RUN mvn -B -DskipTests dependency:go-offline

# Agora copia o código
COPY src ./src

# Build do JAR gordo, pulando testes
RUN mvn -B -DskipTests clean package spring-boot:repackage

# Descobre o JAR final e copia para /app/app.jar dentro do próprio estágio
RUN JAR_FILE="$(ls target/*-SNAPSHOT.jar 2>/dev/null || ls target/*.jar 2>/dev/null | head -n1)" \
    && cp "$JAR_FILE" /app/app.jar

# =======================
# STAGE 2: RUNTIME
# =======================
FROM eclipse-temurin:21-jre

WORKDIR /app

# Copiamos o jar empacotado do estágio de build
COPY --from=build /app/app.jar /app/app.jar

EXPOSE 8080

# Permite passar flags de JVM via env
ENV JAVA_OPTS=""

# Sobe a aplicação
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
