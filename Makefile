#
# Makefile to build and push docker images
#
# This Makefile assumes that the current folder has a secret file called .env which contains:
#    export API_KEY=...
#

IMAGE_NAME=lab-docker
ifndef NAMESPACE
    NAMESPACE=nyu_edu
endif
ifndef REGISTRY
    REGISTRY=registry.ng.bluemix.net
endif

all: build push clean

build:
	$(info Building $(IMAGE_NAME) Image...)
	docker build --rm -t $(IMAGE_NAME) .

push:
	$(info Pushing $(IMAGE_NAME) to Bluemix Registry...)
	docker tag $(IMAGE_NAME) $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME)
	docker push $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME)
	docker rmi $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME)

clean:
	$(info Checking for untagged images)
	docker rmi $$(docker images -q -f dangling=true)

run:
	$(info Running $(IMAGE_NAME) Service...)
	docker run --rm -p 5000:5000 $(IMAGE_NAME)

debug:
	$(info Debugging $(IMAGE_NAME) Service...)
	docker run -it --rm -p 5000:5000 $(IMAGE_NAME) /bin/sh
