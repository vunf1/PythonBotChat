CONTAINER_USER=xraynerd
CONTAINER_NAME=chatbot-coach-client
CONTAINER_VERSION=0.1.0

.PHONY: container
container:
	docker build -t $(CONTAINER_USER)/$(CONTAINER_NAME)\:$(CONTAINER_VERSION) .

.PHONY: start
start:
	docker run --rm -it -p 8080:8080 \
		--name $(CONTAINER_NAME) \
		--volume $(shell pwd)\:/public \
		$(CONTAINER_USER)/$(CONTAINER_NAME)\:$(CONTAINER_VERSION)
