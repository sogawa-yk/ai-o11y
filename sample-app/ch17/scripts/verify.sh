#!/bin/bash
set -euo pipefail
NS=aio11y-book
POD=$(kubectl -n $NS get pod -l book.aio11y/chapter=17 -o name | head -1)
echo "Pod: $POD"
for i in 1 2 3 4 5; do
  kubectl -n $NS exec "$POD" -- python -c "
import urllib.request, json
req=urllib.request.Request('http://localhost:8000/plan',
    data=json.dumps({'city':'Tokyo','days':3,'keywords':['寺院']}).encode(),
    headers={'Content-Type':'application/json'})
urllib.request.urlopen(req).read()
print('/plan OK')
"
done
sleep 15
echo "Prometheus: travel_helper_llm_tokens_sum"
kubectl -n observability exec prometheus-prometheus-kube-prometheus-prometheus-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=sum(rate(travel_helper_llm_tokens_sum%7Bjob%3D%22travel-helper-ch17%22%7D%5B5m%5D))%20by%20(direction)'
echo
echo "verify OK"
