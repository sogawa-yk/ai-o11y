#!/bin/bash
set -euo pipefail
NS=aio11y-book
POD=$(kubectl -n $NS get pod -l book.aio11y/chapter=14 -o name | head -1)
echo "Pod: $POD"
for i in 1 2 3; do
  kubectl -n $NS exec "$POD" -- python -c "
import urllib.request, json
req=urllib.request.Request('http://localhost:8000/plan',
    data=json.dumps({'city':'Kyoto','days':2,'keywords':['寺院']}).encode(),
    headers={'Content-Type':'application/json'})
print(urllib.request.urlopen(req).read().decode())
"
done
echo
echo "Tempo: service.name=travel-helper-ch14"
kubectl -n observability exec tempo-0 -- wget -qO- "http://localhost:3200/api/search?tags=service.name%3Dtravel-helper-ch14&limit=3"
echo
echo "verify OK (LLM_MODE=mock for credential-less verification)"
