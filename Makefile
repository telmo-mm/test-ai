.PHONY: help build up down logs shell clean dev prod

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker image
	docker-compose build

dev: ## Start development environment (SQLite)
	docker-compose -f docker-compose.dev.yml up --build

prod: ## Start production environment (PostgreSQL)
	docker-compose up --build -d

up: ## Start the services
	docker-compose up -d

down: ## Stop the services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

shell: ## Access the app container shell
	docker-compose exec app bash

clean: ## Clean up containers, volumes, and images
	docker-compose down -v
	docker system prune -f

setup: ## Initial setup - copy env file
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your TMDB API key."; \
	else \
		echo ".env file already exists."; \
	fi

# Development workflow
dev-setup: setup build ## Complete development setup
	@echo "Development environment is ready!"
	@echo "1. Edit .env file with your TMDB API key"
	@echo "2. Run 'make dev' to start the development server"
	@echo "3. Open http://localhost:8000 in your browser"
