#!/bin/bash

set -euo pipefail

echo "▶️ Testing fallback route..."

if ! lsof -iTCP:9090 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Starting port-forward to istio-ingressgateway (80 -> 9090)..."
  kubectl -n istio-system port-forward svc/istio-ingressgateway 9090:80 >/tmp/pf-istio-9090.log 2>&1 &
  sleep 2
fi

RESP_BEFORE=$(curl -s http://localhost:9090/ping || true)
echo "Before kill: $RESP_BEFORE"

echo "Scaling v1 to 0 replicas to force failure..."
kubectl scale deploy booking-service-v1 --replicas=0 | cat

echo "Waiting for v1 pods to terminate..."
for i in {1..30}; do
  COUNT=$(kubectl get pods -l app=booking-service-v1 --no-headers 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$COUNT" == "0" ]]; then
    break
  fi
  sleep 1
done

OK=false
for i in {1..10}; do
  RESP_AFTER=$(curl -s --max-time 3 http://localhost:9090/ping || true)
  echo "Attempt $i: $RESP_AFTER"
  if [[ "$RESP_AFTER" == *"v2"* ]]; then
    OK=true
    break
  fi
  sleep 1
done

if [[ "$OK" == "true" ]]; then
  echo "✔️ Fallback to v2 works"
else
  echo "Fallback did not route to v2" >&2
  exit 1
fi

echo "Restoring v1 replicas to 1..."
kubectl scale deploy booking-service-v1 --replicas=1 | cat
