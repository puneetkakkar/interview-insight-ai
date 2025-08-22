.PHONY: help dev-up dev-down dev-logs test test-env test-down prod-up prod-down prod-logs clean format lint migrate revision upgrade coverage coverage-clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development environment commands
dev-up: ## Start development environment
	docker compose -f docker/dev/docker-compose.dev.yml up -d --build

dev-down: ## Stop development environment
	docker compose -f docker/dev/docker-compose.dev.yml down

dev-logs: ## Tail development logs
	docker compose -f docker/dev/docker-compose.dev.yml logs -f

# Testing commands
test: ## Run all tests locally
	uv run pytest tests/ -v

test-all: ## Run all tests with coverage
	uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

test-env: ## Run tests in dedicated testing environment
	@echo "Starting testing environment..."
	docker compose -f docker/test/docker-compose.test.yml up -d --build
	@echo "Waiting for containers to be ready..."
	@sleep 10
	@echo "Creating virtual environment inside container..."
	docker compose -f docker/test/docker-compose.test.yml exec -T api-test uv venv
	@echo "Installing test dependencies..."
	docker compose -f docker/test/docker-compose.test.yml exec -T api-test uv pip install pytest pytest-asyncio pytest-mock pytest-cov faker aiosqlite
	@echo "Running tests..."
	docker compose -f docker/test/docker-compose.test.yml exec -T api-test uv run --active pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v
	@echo "Tests completed. Stopping testing environment..."
	@$(MAKE) test-down

coverage: ## Run tests with coverage report inside API container
	@echo "Starting development environment for coverage..."
	@$(MAKE) dev-up
	@echo "Installing test dependencies..."
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv pip install pytest pytest-cov pytest-asyncio pytest-mock faker aiosqlite
	@echo "Running tests with coverage..."
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated. You can find HTML report in htmlcov/ directory."
	@echo "Note: Development environment is still running. Use 'make dev-down' to stop it when done."

coverage-clean: ## Run tests with coverage report and clean up environment
	@echo "Starting development environment for coverage..."
	@$(MAKE) dev-up
	@echo "Installing test dependencies..."
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv pip install pytest pytest-cov pytest-asyncio pytest-mock faker aiosqlite
	@echo "Running tests with coverage..."
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated. You can find HTML report in htmlcov/ directory."
	@echo "Cleaning up development environment..."
	@$(MAKE) dev-down

test-down: ## Stop testing environment
	docker compose -f docker/test/docker-compose.test.yml down -v

# Production environment commands
prod-up: ## Start production environment
	docker compose -f docker/prod/docker-compose.prod.yml up -d --build

prod-down: ## Stop production environment
	docker compose -f docker/prod/docker-compose.prod.yml down

prod-logs: ## Tail production logs
	docker compose -f docker/prod/docker-compose.prod.yml logs -f

# Database migration commands
migrate: ## Create and apply DB migrations inside API container
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run alembic revision --autogenerate
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run alembic upgrade head

revision: ## Create new DB migration inside API container
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run alembic revision --autogenerate

upgrade: ## Apply DB migrations inside API container
	docker compose -f docker/dev/docker-compose.dev.yml exec -T api-dev uv run alembic upgrade head

# Utility commands
clean: ## Remove all containers and volumes for this project
	docker compose -f docker/dev/docker-compose.dev.yml down -v
	docker compose -f docker/test/docker-compose.test.yml down -v
	docker compose -f docker/prod/docker-compose.prod.yml down -v
	docker system prune -f

format: ## Run formatter/linter fixes
	uv run ruff --fix .

lint: ## Run linter
	uv run ruff .
