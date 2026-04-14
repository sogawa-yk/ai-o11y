CHAPTER := 11
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: build deploy verify clean

# ConfigMap方式でコード配布するためイメージビルドは不要。
# development-guidelines.mdの標準ターゲット整合のためno-opで用意する。
build:
	@echo "ch$(CHAPTER) uses ConfigMap-based code distribution (no image build)."

deploy:
	kubectl apply -f k8s/configmap.yaml -f k8s/app-code.yaml -f k8s/deployment.yaml -n $(NS)
	# 実Secretは読者が secret.yaml を作成して適用する。テンプレは k8s/secret.example.yaml を参照。
	kubectl rollout status deployment/ch$(CHAPTER)-agent -n $(NS) --timeout=180s
verify:
	./scripts/verify.sh
clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap,secret --ignore-not-found
