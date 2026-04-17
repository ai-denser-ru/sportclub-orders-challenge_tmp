.PHONY: test-backend test-frontend test-all docker-up

test-backend:
	cd backend && uv run pytest

test-frontend:
	cd frontend && npm run test

test-all: test-backend test-frontend

docker-up:
	docker compose up --build
