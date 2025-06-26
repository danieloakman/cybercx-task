.PHONY: install install-dev start dev format lint test

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

start:
	python main.py

# Development mode with auto-reload
dev:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Format code with black
format:
	black .

# Lint code with flake8
lint:
	flake8 *.py tests/*.py

# Run tests
test:
	pytest tests/ -v --cov=main --cov-report=term-missing
