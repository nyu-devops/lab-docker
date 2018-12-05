#
# Makefile to deploy to Kubernetes
#

all: deploy

deploy:
	$(info Deploying to Kubernetes...)
	kubectl delete -f deployment.yaml
	kubectl create -f deployment.yaml --record
	@echo "Complete"

service:
	$(info Creatng Service in Kubernetes...)
	kubectl apply -f service.yaml --record
	@echo "Complete"

secrets:
	$(info Creating Secrets in Kubernetes...)
	kubectl apply -f secret.yaml --record
	@echo "Complete"

ingress:
	$(info Deploying Ingress to Kubernetes...)
	kubectl apply -f ingress.yaml --record
	@echo "Complete"
