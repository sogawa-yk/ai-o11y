CHAPTER := 17
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: build deploy verify clean
build:
	@echo "ch$(CHAPTER) uses ConfigMap-based code distribution (no image build)."
deploy:
	kubectl create configmap travel-helper-ch17-code \
	  --from-file=agent.py=agent.py --from-file=otel_setup.py=otel_setup.py \
	  --from-file=tools.py=tools.py --from-file=requirements.txt=requirements.txt \
	  -n $(NS) --dry-run=client -o yaml \
	  | kubectl label --local -f - $(LABEL) app.kubernetes.io/name=travel-helper app.kubernetes.io/part-of=aio11y-book book.aio11y/owned-by=book -o yaml \
	  | kubectl apply -f -
	kubectl apply -f k8s/configmap.yaml -f k8s/deployment.yaml -n $(NS)
	kubectl rollout status deployment/ch$(CHAPTER)-agent -n $(NS) --timeout=180s
verify:
	./scripts/verify.sh
clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap --ignore-not-found
