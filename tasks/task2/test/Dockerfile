FROM debian:bullseye-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY init-fixtures*.sql regress.sh ./
RUN chmod +x regress.sh

ENTRYPOINT ["./regress.sh"]
