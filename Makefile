.PHONY: install start-api start-frontend test test-api test-frontend lint

install:
	pip install -r requirements.txt

start-api:
	cd api && fastapi run main.py --port 8001

start-frontend:
	cd frontend && python manage.py runserver

test:
	pytest

test-api:
	cd api && pytest

test-frontend:
	pytest frontend

lint:
	cd api && pylint --fail-under=8 .
	cd frontend && pylint --fail-under=8 .

migrate:
	cd api && alembic upgrade head

check-migrations:
	cd api && alembic check
