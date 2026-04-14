CHAPTER := 15
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: build deploy verify clean
build:
	@echo "ch$(CHAPTER) uses ConfigMap-based code distribution (no image build)."
deploy:
	kubectl apply -f ../../collector-config/deploy/collector-deployment.yaml -n $(NS)
	# 実際のCollector設定ファイルをConfigMapに上書き
	kubectl create configmap ch15-collector-config \
	  --from-file=config.yaml=../../collector-config/ch15-add-langfuse/config.yaml \
	  -n $(NS) --dry-run=client -o yaml \
	  | kubectl label --local -f - app.kubernetes.io/name=ch15-collector app.kubernetes.io/part-of=aio11y-book book.aio11y/owned-by=book book.aio11y/chapter=15 -o yaml \
	  | kubectl replace -f -
	kubectl rollout restart deploy/ch15-collector -n $(NS)
	kubectl apply -f k8s/ -n $(NS)
	kubectl rollout status deploy/ch15-collector -n $(NS) --timeout=120s
	kubectl rollout status deploy/ch15-agent -n $(NS) --timeout=180s
verify:
	./scripts/verify.sh
clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap,secret --ignore-not-found
