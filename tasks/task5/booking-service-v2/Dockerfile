# Используем официальный минимальный образ Go
FROM golang:1.21-alpine

RUN apk add --no-cache curl

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем Go-файл и скрипт проверки DNS
COPY main.go .
COPY check-dns.sh .

RUN chmod +x check-dns.sh

RUN go build -o booking-service main.go

EXPOSE 8080

CMD ["./booking-service"]
