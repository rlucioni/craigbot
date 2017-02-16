.PHONY: quality requirements run

quality:
	flake8

requirements:
	pip install -r requirements.txt

run:
	./bot.py
