.PHONY: image logs prune pull push run shell stop

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

run: ## Start a container derived from the rlucioni/apartments image
	docker run -d --name apartments rlucioni/apartments

shell: ## Open a shell on a running container
	docker exec -it apartments /bin/bash

stop: ## Stop a running container
	docker stop apartments
