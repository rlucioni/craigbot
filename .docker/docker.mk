.PHONY: connect image logs prune pull push quality run shell stop

connect: ## Connect to a Docker host running on a cloud service provider (e.g., DigitalOcean)
	eval $$(docker-machine env craigbot)

image: ## Build an rlucioni/craigbot image
	docker build -f .docker/Dockerfile -t rlucioni/craigbot:latest .

logs: ## Tail a running container's logs
	docker logs -f craigbot

prune: ## Delete stopped containers and dangling images
	docker system prune

pull: ## Update the rlucioni/craigbot image
	docker pull rlucioni/craigbot

push: ## Push the rlucioni/craigbot image to Docker Hub
	docker push rlucioni/craigbot

quality: ## Run quality checks
	docker run rlucioni/craigbot flake8

run: ## Start a container derived from the rlucioni/craigbot image
	docker run -d --name craigbot --env-file .docker/env --restart on-failure rlucioni/craigbot

shell: ## Open a shell on a running container
	docker exec -it craigbot /usr/bin/env bash

stop: ## Stop a running container
	docker stop craigbot
