.PHONY: help migrate revision upgrade test clean \
	dev-up dev-down dev-logs dev-build \
	prod-up prod-down prod-logs prod-build \
	format lint test-unit test-integration test-all coverage

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

migrate: ## Create and apply DB migrations inside API container
	docker compose exec -T api uv run alembic revision --autogenerate
	docker compose exec -T api uv run alembic upgrade head

revision: ## Create new DB migration inside API container
	docker compose exec -T api uv run alembic revision --autogenerate

upgrade: ## Apply DB migrations inside API container
	docker compose exec -T api uv run alembic upgrade head

test: ## Run all tests inside API container
	docker compose exec -T api sh -lc 'uv pip install -q ".[test]" >/dev/null 2>&1 || true && uv run pytest'

test-unit: ## Run unit tests only inside API container
	docker compose exec -T api sh -lc 'uv pip install -q ".[test]" >/dev/null 2>&1 || true && uv run pytest tests/unit/'

test-integration: ## Run integration tests only inside API container
	docker compose exec -T api sh -lc 'uv pip install -q ".[test]" >/dev/null 2>&1 || true && uv run pytest tests/integration/'

test-all: ## Run all tests with verbose output inside API container
	docker compose exec -T api sh -lc 'uv pip install -q ".[test]" >/dev/null 2>&1 || true && uv run pytest -v'

coverage: ## Run tests with coverage report inside API container
	docker compose exec -T api sh -lc 'uv pip install -q ".[test]" >/dev/null 2>&1 || true && uv run pytest --cov=src --cov-report=term-missing --cov-report=html'

clean: ## Remove containers and volumes for this project
	docker compose down -v
	docker system prune -f

# New targets for environments
dev-up: ## Start dev stack
	docker compose up -d

dev-down: ## Stop dev stack
	docker compose down

dev-logs: ## Tail dev logs
	docker compose logs -f

dev-build: ## Build dev images
	docker compose build --no-cache

prod-up: ## Start prod stack (no reload)
	ENVIRONMENT=production DEBUG=false RELOAD=false docker compose up -d --build

prod-down: ## Stop prod stack
	docker compose down

prod-logs: ## Tail prod logs
	docker compose logs -f

prod-build: ## Build prod images
	ENVIRONMENT=production DEBUG=false RELOAD=false docker compose build --no-cache

format: ## Run formatter/linter fixes
	uv run ruff --fix .

lint: ## Run linter
	uv run ruff .
