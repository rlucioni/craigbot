.PHONY: connect image logs prune pull push quality run shell stop

connect: ## Connect to a Docker host running on a cloud service provider (e.g., DigitalOcean)
	eval $(docker-machine env apartments)

image: ## Build an rlucioni/apartments image
	docker build -f .docker/Dockerfile -t rlucioni/apartments:latest .

logs: ## Tail a running container's logs
	docker logs -f apartments

prune: ## Delete stopped containers and dangling images
	docker system prune

pull: ## Update the rlucioni/apartments image
	docker pull rlucioni/apartments

push: ## Push the rlucioni/apartments image to Docker Hub
	docker push rlucioni/apartments

quality: ## Run quality checks
	docker run rlucioni/apartments flake8

run: ## Start a container derived from the rlucioni/apartments image
	docker run -d --name apartments --env-file .docker/env rlucioni/apartments

shell: ## Open a shell on a running container
	docker exec -it apartments /bin/bash

stop: ## Stop a running container
	docker stop apartments
