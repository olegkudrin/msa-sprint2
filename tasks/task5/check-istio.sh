#!/bin/bash

set -euo pipefail

echo "▶️ Проверка установки Istio..."
kubectl get pods -n istio-system | cat

echo "▶️ Включаем инъекцию сайдкара в default..."
kubectl label namespace default istio-injection=enabled --overwrite

echo "▶️ Проверка Istio инъекции в default namespace..."
kubectl get namespace default -o json | jq -r '.metadata.labels."istio-injection"'
