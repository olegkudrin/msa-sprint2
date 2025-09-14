#!/bin/bash

set -euo pipefail

echo "▶️ Проверка Feature Flag (X-Feature-Enabled: true)..."

if ! lsof -iTCP:9090 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Starting port-forward to istio-ingressgateway (80 -> 9090)..."
  kubectl -n istio-system port-forward svc/istio-ingressgateway 9090:80 >/tmp/pf-istio-9090.log 2>&1 &
  sleep 2
fi

RESP=$(curl -s -H "X-Feature-Enabled: true" http://localhost:9090/ping)
echo "Response: $RESP"
if [[ "$RESP" != *"v2"* ]]; then
  echo "Feature flag routing failed" >&2
  exit 1
fi
echo "✔️ Feature flag routes to v2"
