#!/bin/bash
set -euo pipefail
NS=aio11y-book
POD=$(kubectl -n $NS get pod -l book.aio11y/chapter=11 -o name | head -1)
echo "Pod: $POD"
for i in 1 2 3; do
  kubectl -n $NS exec "$POD" -- python -c "
import urllib.request, json
req=urllib.request.Request('http://localhost:8000/plan',
    data=json.dumps({'city':'Nara','days':2,'keywords':['寺院','和食']}).encode(),
    headers={'Content-Type':'application/json'})
print(urllib.request.urlopen(req).read().decode())
"
done
echo
echo "OTel trace は Tempo で確認: service.name=travel-helper-ch11"
echo "Langfuse は Web UI で確認: http://langfuse-web.langfuse:3000"
echo
echo "verify OK (Langfuse credentials 未設定時は Langfuse 記録はスキップされる)"
