.PHONY: help install dev-install test lint format type-check clean docker-up docker-down docker-logs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements/base.txt

dev-install: ## Install development dependencies
	pip install -r requirements/dev.txt
	pre-commit install

test: ## Run tests
	pytest tests/ -v --cov=ai_travel_planner --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	pytest-watch tests/ -- -v

lint: ## Run linting
	flake8 .
	mypy .

format: ## Format code
	black .
	isort .

type-check: ## Run type checking
	mypy .

clean: ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

docker-up: ## Start development services
	docker-compose -f docker/docker-compose.dev.yml up -d

docker-down: ## Stop development services
	docker-compose -f docker/docker-compose.dev.yml down

docker-logs: ## View service logs
	docker-compose -f docker/docker-compose.dev.yml logs -f

docker-rebuild: ## Rebuild and restart services
	docker-compose -f docker/docker-compose.dev.yml down
	docker-compose -f docker/docker-compose.dev.yml build --no-cache
	docker-compose -f docker/docker-compose.dev.yml up -d

setup-dev: ## Run development environment setup
	./scripts/setup-dev.sh

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create new migration
	alembic revision --autogenerate -m "$(name)"

serve: ## Start development server
	uvicorn services.api_gateway.main:app --reload --host 0.0.0.0 --port 8080