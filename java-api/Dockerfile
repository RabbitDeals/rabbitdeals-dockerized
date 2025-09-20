FROM maven:3.9.8-eclipse-temurin-21 AS build
WORKDIR /app
ARG GIT_REF=main
RUN git clone https://github.com/RabbitDeals/rabbitdeals-api.git . \
 && git checkout $GIT_REF
RUN mvn -B -DskipTests clean package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
