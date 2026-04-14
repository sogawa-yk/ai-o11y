#!/bin/bash
set -euo pipefail
NS=aio11y-book
POD=$(kubectl -n $NS get pod -l book.aio11y/chapter=13 -o name | head -1)
echo "Pod: $POD"
for i in 1 2 3 4 5; do
  kubectl -n $NS exec "$POD" -- python -c "
import urllib.request, json
req=urllib.request.Request('http://localhost:8000/plan',
    data=json.dumps({'city':'Tokyo','days':3,'keywords':['寺院','和食']}).encode(),
    headers={'Content-Type':'application/json'})
print(urllib.request.urlopen(req).read().decode())
"
done
echo
echo "Tempo: service.name=travel-helper-ch13"
kubectl -n observability exec tempo-0 -- wget -qO- "http://localhost:3200/api/search?tags=service.name%3Dtravel-helper-ch13&limit=3"
echo
echo "Prometheus: travel_helper_requests_total"
kubectl -n observability exec prometheus-prometheus-kube-prometheus-prometheus-0 -c prometheus -- wget -qO- "http://localhost:9090/api/v1/query?query=travel_helper_requests_total"
echo
echo "verify OK"
