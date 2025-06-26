.PHONY: install start dev

install:
	pip install -r requirements.txt

start: install
	python main.py

# Development mode with auto-reload
dev: install
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload
