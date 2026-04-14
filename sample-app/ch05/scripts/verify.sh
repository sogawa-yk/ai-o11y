#!/bin/bash
set -euo pipefail
NS=aio11y-book
POD=$(kubectl -n $NS get pod -l book.aio11y/chapter=05 -o name | head -1)
echo "Pod: $POD"
for i in 1 2 3; do
  kubectl -n $NS exec "$POD" -- python -c "
import urllib.request, json
req=urllib.request.Request('http://localhost:8000/plan',
    data=json.dumps({'city':'Osaka','days':3,'keywords':['寺院']}).encode(),
    headers={'Content-Type':'application/json'})
print(urllib.request.urlopen(req).read().decode())
"
done
sleep 12
echo "Tempo:"
kubectl -n observability exec tempo-0 -- wget -qO- "http://localhost:3200/api/search?tags=service.name%3Dtravel-helper-ch05&limit=3"
echo
echo "Prometheus:"
kubectl -n observability exec prometheus-prometheus-kube-prometheus-prometheus-0 -c prometheus -- wget -qO- "http://localhost:9090/api/v1/query?query=travel_helper_requests_total"
echo
echo "verify OK"
