.PHONY: quality requirements

quality:
	flake8

requirements:
	pip install -r requirements.txt
