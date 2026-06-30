# Istio Canary, Fallback, Retries/Circuit Breaking, Feature Flag

## Изменения

- Добавлен Gateway и VirtualService с канареечной маршрутизацией 90/10 и fallbacks (virtual-service.yaml)
- Добавлены DestinationRule для v1 и v2 с retry/circuit breaking (destination-rule.yaml)
- Добавлен EnvoyFilter (Lua) для фича-флага X-Feature-Enabled: true → принудительно в v2 (envoy-filter.yaml)
- В Helm шаблоны добавлены метки service: booking-service и version: <тег версии>
- Скрипты проверки обновлены: порт‑форвардинг ingress на 9090, валидации распределения / фичи / фолбэка.

## Развертывание

1. Установить Istio:
  - istioctl install -y
  - kubectl label namespace default istio-injection=enabled --overwrite

2. Собрать образы:
  - docker build -t booking-service:v1 booking-service-v1
  - docker build -t booking-service:v2 booking-service-v2

3. Задеплоить две версии:
  - helm upgrade --install booking-service-v1 helm/booking-service -f values-v1.yaml
  - helm upgrade --install booking-service-v2 helm/booking-service -f values-v2.yaml

4. Общий сервис
  - kubectl apply -f shared-service.yaml

5. Конфигурация Istio:
  - kubectl apply -f virtual-service.yaml
  - kubectl apply -f destination-rule.yaml
  - kubectl apply -f envoy-filter.yaml

## Проверки

- ./check-istio.sh
- ./check-canary.sh
- ./check-fallback.sh
- ./check-feature-flag.sh
