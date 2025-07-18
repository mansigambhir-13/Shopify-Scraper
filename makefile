# =============================================================================
# Shopify Store Insights Fetcher - Development Makefile
# =============================================================================

# Variables
PYTHON := python
PIP := pip
VENV := venv
APP_NAME := shopify-insights-fetcher
DB_FILE := shopify_insights.db
DOCKER_IMAGE := $(APP_NAME)
DOCKER_TAG := latest

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# =============================================================================
# HELP
# =============================================================================

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Shopify Store Insights Fetcher - Development Commands$(NC)"
	@echo "======================================================"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make setup          # Complete project setup"
	@echo "  make dev            # Start development server"
	@echo "  make test           # Run all tests"
	@echo "  make clean          # Clean all generated files"

# =============================================================================
# SETUP COMMANDS
# =============================================================================

.PHONY: setup
setup: ## Complete project setup for new developers
	@echo "$(BLUE)Setting up Shopify Store Insights Fetcher...$(NC)"
	$(MAKE) venv
	$(MAKE) install
	$(MAKE) install-dev
	$(MAKE) setup-pre-commit
	$(MAKE) setup-env
	$(MAKE) test-db
	@echo "$(GREEN)✅ Setup complete! Run 'make dev' to start development server$(NC)"

.PHONY: venv
venv: ## Create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✅ Virtual environment created$(NC)"
	@echo "$(YELLOW)Activate with: source $(VENV)/bin/activate (Linux/Mac) or $(VENV)\\Scripts\\activate (Windows)$(NC)"

.PHONY: install
install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Production dependencies installed$(NC)"

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✅ Development dependencies installed$(NC)"

.PHONY: setup-pre-commit
setup-pre-commit: ## Setup pre-commit hooks
	@echo "$(BLUE)Setting up pre-commit hooks...$(NC)"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "$(GREEN)✅ Pre-commit hooks installed$(NC)"

.PHONY: setup-env
setup-env: ## Setup environment configuration
	@echo "$(BLUE)Setting up environment configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env file...$(NC)"; \
		$(PYTHON) setup_env.py; \
	else \
		echo "$(YELLOW).env file already exists$(NC)"; \
		$(PYTHON) validate_env.py; \
	fi

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

.PHONY: dev
dev: ## Start development server with auto-reload
	@echo "$(BLUE)Starting development server...$(NC)"
	@echo "$(YELLOW)API will be available at: http://localhost:8000$(NC)"
	@echo "$(YELLOW)API docs will be available at: http://localhost:8000/docs$(NC)"
	$(PYTHON) main.py

.PHONY: dev-debug
dev-debug: ## Start development server with debug logging
	@echo "$(BLUE)Starting development server with debug logging...$(NC)"
	LOG_LEVEL=DEBUG $(PYTHON) main.py

.PHONY: shell
shell: ## Start Python shell with app context
	@echo "$(BLUE)Starting Python shell...$(NC)"
	$(PYTHON) -c "from app import *; import asyncio; print('App modules loaded. Use asyncio.run() for async functions.')"

.PHONY: notebook
notebook: ## Start Jupyter notebook for development
	@echo "$(BLUE)Starting Jupyter notebook...$(NC)"
	jupyter notebook

# =============================================================================
# DATABASE COMMANDS
# =============================================================================

.PHONY: db-create
db-create: ## Create database tables
	@echo "$(BLUE)Creating database tables...$(NC)"
	$(PYTHON) -c "import asyncio; from app.database.database import init_db; asyncio.run(init_db())"
	@echo "$(GREEN)✅ Database tables created$(NC)"

.PHONY: db-reset
db-reset: ## Reset database (delete and recreate)
	@echo "$(RED)Resetting database...$(NC)"
	@if [ -f $(DB_FILE) ]; then rm $(DB_FILE); echo "$(YELLOW)Deleted existing database$(NC)"; fi
	$(MAKE) db-create
	@echo "$(GREEN)✅ Database reset complete$(NC)"

.PHONY: db-backup
db-backup: ## Backup database
	@echo "$(BLUE)Backing up database...$(NC)"
	@if [ -f $(DB_FILE) ]; then \
		cp $(DB_FILE) $(DB_FILE).backup.$(shell date +%Y%m%d_%H%M%S); \
		echo "$(GREEN)✅ Database backed up$(NC)"; \
	else \
		echo "$(YELLOW)No database file found$(NC)"; \
	fi

.PHONY: db-browse
db-browse: ## Open database browser
	@echo "$(BLUE)Opening database browser...$(NC)"
	@if [ -f $(DB_FILE) ]; then \
		sqlite_web $(DB_FILE) & \
		echo "$(GREEN)✅ Database browser started at http://localhost:8080$(NC)"; \
	else \
		echo "$(RED)Database file not found. Run 'make db-create' first$(NC)"; \
	fi

.PHONY: test-db
test-db: ## Test database connection
	@echo "$(BLUE)Testing database connection...$(NC)"
	$(PYTHON) test_simple_sqlite.py

# =============================================================================
# TESTING COMMANDS
# =============================================================================

.PHONY: test
test: ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	pytest

.PHONY: test-fast
test-fast: ## Run only fast tests (unit tests)
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest -m "not slow and not integration"

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest -m unit

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest -m integration

.PHONY: test-api
test-api: ## Run API tests only
	@echo "$(BLUE)Running API tests...$(NC)"
	pytest -m api

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(NC)"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	ptw --runner "pytest -x"

# =============================================================================
# CODE QUALITY COMMANDS
# =============================================================================

.PHONY: format
format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	black app/ tests/ *.py
	isort app/ tests/ *.py
	@echo "$(GREEN)✅ Code formatted$(NC)"

.PHONY: lint
lint: ## Run all linting checks
	@echo "$(BLUE)Running linting checks...$(NC)"
	flake8 app/ tests/
	black --check app/ tests/ *.py
	isort --check-only app/ tests/ *.py
	@echo "$(GREEN)✅ Linting checks passed$(NC)"

.PHONY: mypy
mypy: ## Run type checking
	@echo "$(BLUE)Running type checking...$(NC)"
	mypy app/
	@echo "$(GREEN)✅ Type checking passed$(NC)"

.PHONY: security
security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r app/
	safety check
	@echo "$(GREEN)✅ Security checks passed$(NC)"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

.PHONY: quality
quality: lint mypy security ## Run all code quality checks

# =============================================================================
# DOCKER COMMANDS
# =============================================================================

.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✅ Docker image built$(NC)"

.PHONY: docker-run
docker-run: ## Run application in Docker
	@echo "$(BLUE)Running application in Docker...$(NC)"
	docker run -p 8000:8000 -v $(PWD)/data:/app/data $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker-compose-up
docker-compose-up: ## Start all services with docker-compose
	@echo "$(BLUE)Starting services with docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started$(NC)"

.PHONY: docker-compose-down
docker-compose-down: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Services stopped$(NC)"

.PHONY: docker-logs
docker-logs: ## View Docker logs
	@echo "$(BLUE)Viewing Docker logs...$(NC)"
	docker-compose logs -f

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

.PHONY: clean
clean: ## Clean all generated files
	@echo "$(BLUE)Cleaning generated files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage
	rm -f *.log
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

.PHONY: clean-db
clean-db: ## Clean database files
	@echo "$(BLUE)Cleaning database files...$(NC)"
	rm -f *.db *.sqlite *.sqlite3
	@echo "$(GREEN)✅ Database files cleaned$(NC)"

.PHONY: clean-all
clean-all: clean clean-db ## Clean everything including database
	@echo "$(GREEN)✅ Complete cleanup finished$(NC)"

.PHONY: logs
logs: ## View application logs
	@echo "$(BLUE)Viewing application logs...$(NC)"
	@if [ -d logs ]; then \
		tail -f logs/*.log; \
	else \
		echo "$(YELLOW)No logs directory found$(NC)"; \
	fi

.PHONY: requirements
requirements: ## Update requirements files
	@echo "$(BLUE)Updating requirements...$(NC)"
	pip-compile requirements.in
	pip-compile requirements-dev.in
	@echo "$(GREEN)✅ Requirements updated$(NC)"

.PHONY: docs
docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "$(YELLOW)Documentation features not yet implemented$(NC)"

# =============================================================================
# VALIDATION COMMANDS
# =============================================================================

.PHONY: validate
validate: ## Validate project configuration
	@echo "$(BLUE)Validating project configuration...$(NC)"
	$(PYTHON) validate_env.py
	$(MAKE) test-db
	@echo "$(GREEN)✅ Project validation complete$(NC)"

.PHONY: health
health: ## Check application health
	@echo "$(BLUE)Checking application health...$(NC)"
	@curl -f http://localhost:8000/health || echo "$(RED)Application not running$(NC)"

# =============================================================================
# SUBMISSION COMMANDS
# =============================================================================

.PHONY: submission-check
submission-check: ## Check if project is ready for submission
	@echo "$(BLUE)Checking submission readiness...$(NC)"
	$(MAKE) quality
	$(MAKE) test
	$(MAKE) validate
	@echo "$(GREEN)✅ Project ready for submission!$(NC)"

.PHONY: demo
demo: ## Run demo with sample data
	@echo "$(BLUE)Running demo...$(NC)"
	curl -X POST "http://localhost:8000/api/v1/extract-insights" \
		-H "Content-Type: application/json" \
		-d '{"website_url": "https://gymshark.com"}' | python -m json.tool

# =============================================================================
# DEFAULT TARGET
# =============================================================================

.DEFAULT_GOAL := help