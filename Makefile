.PHONY: install run-api run-frontend test coverage lint format type-check docker-build docker-up docker-down clean reset-db

install:
	python -m pip install -U pip
	python -m pip install -r requirements.txt

run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	streamlit run frontend/Home.py --server.port 8501

test:
	pytest -q

coverage:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check .

format:
	black .

type-check:
	mypy app

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	rm -rf .pytest_cache htmlcov .coverage data/chroma data/uploads data/metadata

reset-db:
	python scripts/reset_vector_database.py
