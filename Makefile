.PHONY: all format lint

all: help

help:
	@echo "make"

	@echo "    format"
	@echo "        Apply black formatting to code."
	@echo "    lint"
	@echo "        Lint code with ruff, and check if black formatter should be applied."

format:
	poetry run black .
	poetry run ruff . --fix

lint:
	poetry run black . --check
	poetry run ruff .
