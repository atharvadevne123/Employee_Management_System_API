.PHONY: install test lint run migrate seed docker-build docker-up docker-down clean

install:
	pip install -r requirements.txt

test:
	USE_SQLITE=True pytest tests/ -v --tb=short --cov=employees --cov=attendance --cov-report=term-missing

lint:
	ruff check . --select E,F,W,I --ignore E501

lint-fix:
	ruff check . --select E,F,W,I --ignore E501 --fix

migrate:
	USE_SQLITE=True python manage.py migrate

seed:
	USE_SQLITE=True python manage.py seed_data --count 50

run:
	USE_SQLITE=True python manage.py runserver

check:
	USE_SQLITE=True python manage.py check

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f api

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f db.sqlite3 coverage.xml .coverage
