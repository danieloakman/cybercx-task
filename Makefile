.PHONY: install install-dev start dev format lint test

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Alternative if using pyproject.toml
# install-dev:
# 	pip install -e ".[dev]"

start: install
	python main.py

# Development mode with auto-reload
dev: install-dev
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Format code with black
format: install-dev
	black .

# Lint code with flake8
lint: install-dev
	flake8 .

# Run tests
test: install-dev
	pytest tests/ -v --cov=main --cov-report=term-missing
