.DEFAULT_GOAL := image

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message
	@echo "Please run \`make <target>\` where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

attach: ## Open a shell on a running craigbot container
	docker exec -it craigbot /usr/bin/env bash

debug: ## Run and attach to container for debugging
	docker run -it --privileged --env-file .docker/env -v craigbot_data:/var/db rlucioni/craigbot

image: ## Build an rlucioni/craigbot image
	docker build -t rlucioni/craigbot:latest .

logs: ## Tail a running container's logs
	docker logs -f craigbot

prune: ## Delete stopped containers and dangling images
	docker system prune -f

pull: ## Update the rlucioni/craigbot image
	docker pull rlucioni/craigbot

run: ## Start a container derived from the rlucioni/craigbot image
	docker run -d --privileged --name craigbot --env-file .docker/env -v craigbot_data:/var/db --restart on-failure rlucioni/craigbot

shell: ## Open a shell on a new container
	docker run -it --privileged -v craigbot_data:/var/db rlucioni/craigbot:latest /usr/bin/env bash

stop: ## Stop a running container
	docker stop craigbot
