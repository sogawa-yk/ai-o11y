CHAPTER := 04
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: deploy verify clean

deploy:
	kubectl apply -f k8s/ -n $(NS)
	kubectl rollout status deployment/ch$(CHAPTER)-agent -n $(NS) --timeout=180s

verify:
	./scripts/verify.sh

clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap --ignore-not-found
