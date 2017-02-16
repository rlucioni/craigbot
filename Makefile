.PHONY: image logs prune quality requirements run shell stop

image:
	docker build -t rlucioni/apartments:latest .

logs:
	docker logs -f apartments

prune:
	docker system prune

quality:
	flake8

requirements:
	pip install -r requirements.txt

run:
	docker run -d --name apartments rlucioni/apartments

shell:
	docker exec -it apartments /bin/bash

stop:
	docker stop apartments
