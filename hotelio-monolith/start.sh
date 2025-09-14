#!/bin/bash

export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost/hotelio
export SPRING_DATASOURCE_USERNAME=hotelio
export SPRING_DATASOURCE_PASSWORD=hotelio

# export BOOKING_SERVICE_EXTERNAL_HOST=booking-service
# export BOOKING_SERVICE_EXTERNAL_PORT=9090

java -jar build/libs/hotelio-monolith-1.0.0.jar
