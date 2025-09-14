# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /app

COPY . /app

COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

CMD /wait && exec python -m booking.service
