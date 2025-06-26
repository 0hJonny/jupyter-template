# Makefile
ORIGIN ?= 0hjohnny
IMAGE_NAME ?= $(ORIGIN)/jupyterhub-minimal
IMAGE_TAG ?= latest
PLATFORMS ?= linux/amd64,linux/arm64
CONFIG_FILE ?= jupyterhub_config.py
BASE_IMAGE ?= quay.io/jupyterhub/jupyterhub:5.3.0

# Сборка для текущей платформы
build:
	docker build \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		-t $(IMAGE_NAME):$(IMAGE_TAG) \
		.

# Сборка для мультиплатформы
buildx:
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		-t $(IMAGE_NAME):$(IMAGE_TAG) \
		--push .

run:
	docker run -it --rm \
		-p 8000:8000 \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(CURDIR)/$(CONFIG_FILE):/srv/jupyterhub/jupyterhub_config.py \
		$(IMAGE_NAME):$(IMAGE_TAG)

prod:
	docker run -d --name jupyterhub \
		--restart unless-stopped \
		--network jupyterhub_network \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(CURDIR)/$(CONFIG_FILE):/srv/jupyterhub/jupyterhub_config.py \
		$(IMAGE_NAME):$(IMAGE_TAG)

push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

release: buildx

clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

# Справка
help:
	@echo "Использование:"
	@echo "  make build [IMAGE_NAME=...] [IMAGE_TAG=...]     - Сборка образа"
	@echo "  make buildx [IMAGE_NAME=...] [IMAGE_TAG=...]    - Мультиплатформенная сборка"
	@echo "  make run [CONFIG_FILE=...]                     - Запуск для тестирования"
	@echo "  make prod [CONFIG_FILE=...]                    - Запуск в production"
	@echo "  make release                                   - Сборка и публикация"
	@echo ""
	@echo "Примеры:"
	@echo "  make build IMAGE_NAME=myreg/jupyterhub IMAGE_TAG=v1.0"
	@echo "  make buildx PLATFORMS=linux/arm64 IMAGE_NAME=myreg/jupyterhub-arm"
	@echo "  make run CONFIG_FILE=config/dev_config.py"

.PHONY: build buildx run prod push release clean help
