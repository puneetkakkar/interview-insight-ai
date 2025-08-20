.PHONY: help up down build migrate revision upgrade test run logs clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start services with docker compose
	docker compose up -d

down: ## Stop and remove services
	docker compose down

build: ## Build docker images
	docker compose build

migrate: ## Create and apply database migrations
	uv run alembic revision --autogenerate
	uv run alembic upgrade head

revision: ## Create new database migration
	uv run alembic revision --autogenerate

upgrade: ## Apply database migrations
	uv run alembic upgrade head

test: ## Run tests
	uv run pytest

run: ## Run development server
	uv run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

logs: ## Show service logs
	docker compose logs -f

clean: ## Clean up docker volumes and containers
	docker compose down -v
	docker system prune -f
