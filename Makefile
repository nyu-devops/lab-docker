#
# Makefile to build and push docker images
#
# This Makefile assumes that the current folder has a secret file called .env which contains:
#    export API_KEY=...
#

# These can be overidden with env vars.
IMAGE_NAME ?= lab-docker

.SILENT:

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

##@ Development

.PHONY: clean
clean:	## Removes all dangling docker images
	$(info Removing all dangling docker images..)
	docker image prune -f

.PHONY: venv
venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	poetry config virtualenvs.in-project true
	poetry shell

.PHONY: install
install: ## Install dependencies
	$(info Installing dependencies...)
	sudo poetry config virtualenvs.create false
	sudo poetry install

.PHONY: lint
lint: ## Run the linter
	$(info Running linting...)
	flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service tests --max-line-length=127

.PHONY: test
test: ## Run the unit tests
	$(info Running tests...)
	export RETRY_COUNT=1; pytest --pspec --cov=service --cov-fail-under=95

##@ Runtime

.PHONY: build
build: ## Build a docker image
	$(info Building $(IMAGE_NAME) Image...)
	docker build --rm --pull -t $(IMAGE_NAME) .

.PHONY: run
run: ## Run the service
	$(info Starting service...)
	honcho start
