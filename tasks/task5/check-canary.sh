#!/bin/bash

set -euo pipefail

echo "▶️ Checking canary release (90% v1, 10% v2)..."

# Ensure port-forward to istio ingressgateway on localhost:9090
if ! lsof -iTCP:9090 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Starting port-forward to istio-ingressgateway (80 -> 9090)..."
  kubectl -n istio-system port-forward svc/istio-ingressgateway 9090:80 >/tmp/pf-istio-9090.log 2>&1 &
  # Give it a moment to start
  sleep 2
fi

V1=0
V2=0

for _ in {1..100}
do
  RESP=$(curl -s http://localhost:9090/ping || true)
  if [[ "$RESP" == *"v2"* ]]; then
    V2=$((V2+1))
  else
    V1=$((V1+1))
  fi
done

echo "v1: $V1, v2: $V2"

# Basic expectation: v1 around 90 and v2 around 10 (tolerate +/- 10)
if [[ $V1 -lt 75 || $V1 -gt 100 ]]; then
  echo "Canary distribution unexpected (v1=$V1, v2=$V2)" >&2
  exit 1
fi

echo "✔️ Canary looks OK"
