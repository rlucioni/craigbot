.PHONY: connect create image kill logs provision prune pull push quality run shell stop

connect: ## Connect to a Docker host running on a DigitalOcean Droplet
	eval $$(docker-machine env craigbot)

create: ## Create a Droplet for hosting Craigbot
	docker-machine create --driver digitalocean --digitalocean-access-token $$(cat ~/.digitalocean-access-token) craigbot

image: ## Build an rlucioni/craigbot image
	docker build -f .docker/Dockerfile -t rlucioni/craigbot:latest .

kill: ## Stop and remove the Droplet hosting craigbot.
	docker-machine stop craigbot && docker-machine rm craigbot

logs: ## Tail a running container's logs
	docker logs -f craigbot

provision: ## Reprovision an existing craigbot machine
	docker-machine provision craigbot

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
