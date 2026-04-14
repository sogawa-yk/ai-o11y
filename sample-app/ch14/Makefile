CHAPTER := 14
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: build deploy verify clean
build:
	@echo "ch$(CHAPTER) uses ConfigMap-based code distribution (no image build)."
deploy:
	kubectl apply -f k8s/configmap.yaml -f k8s/app-code.yaml -f k8s/deployment.yaml -n $(NS)
	kubectl rollout status deployment/ch$(CHAPTER)-agent -n $(NS) --timeout=180s
verify:
	./scripts/verify.sh
clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap,secret --ignore-not-found
