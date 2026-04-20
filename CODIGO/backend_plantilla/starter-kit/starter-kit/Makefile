.PHONY: help install test test-unit test-integration test-security coverage security-scan sonar clean

PROJECT_NAME = mesapass
PYTHON_VERSION = 3.11
VENV_DIR = .venv

help:
	@echo "MESAPASS BACKEND - Test Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install all dependencies"
	@echo "  make install-dev      - Install dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-security    - Run security tests"
	@echo "  make test-watch       - Run tests on file changes"
	@echo ""
	@echo "Coverage:"
	@echo "  make coverage         - Generate coverage report"
	@echo "  make coverage-html    - Generate HTML coverage report"
	@echo ""
	@echo "Security:"
	@echo "  make sec-bandit       - Run Bandit security scan"
	@echo "  make sec-safety       - Check for vulnerable dependencies"
	@echo "  make sec-all          - Run all security checks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run Pylint"
	@echo "  make format           - Format code with Black"
	@echo "  make quality          - Run all quality checks"
	@echo ""
	@echo "SonarQube:"
	@echo "  make sonar            - Run SonarQube analysis"
	@echo "  make sonar-full       - Coverage + Sonar"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove cache and build files"
	@echo "  make clean-all        - Full clean including .venv"
	@echo ""

install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/unit/ -v -m unit

test-integration:
	pytest tests/integration/ -v -m integration

test-security:
	pytest tests/security/ -v -m security

test-all:
	pytest tests/ -v

test-watch:
	pytest-watch tests/ -- -v

coverage:
	pytest tests/ --cov=app --cov-report=term-missing

coverage-html:
	pytest tests/ --cov=app --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

coverage-xml:
	pytest tests/ --cov=app --cov-report=xml

sec-bandit:
	bandit -r app/ -v

sec-bandit-json:
	bandit -r app/ -f json -o bandit-report.json

sec-safety:
	safety check

sec-safety-json:
	safety check --json > safety-report.json || true

sec-all: sec-bandit sec-safety

lint:
	pylint app/ --exit-zero

format:
	black app/ tests/
	isort app/ tests/

quality: lint format

sonar:
	sonar-scanner

sonar-full: coverage-xml sonar
	@echo "SonarQube analysis complete"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete
	find . -type f -name "*.pyc" -delete
	rm -f coverage.xml bandit-report.json safety-report.json pylint-report.json
	rm -rf .eggs/ *.egg-info/ dist/ build/

clean-all: clean
	rm -rf $(VENV_DIR)
	rm -f db.sqlite3 test.db

# Run full test suite with all reports
full-test: clean test coverage sec-all lint
	@echo ""
	@echo "✓ All tests completed"
	@echo "  Coverage: htmlcov/index.html"
	@echo "  Bandit: bandit-report.json"
	@echo "  Safety: safety-report.json"

# Quick test for development
quick:
	pytest tests/ -v --tb=short -x

# Debug mode
debug:
	pytest tests/ -v -s --tb=long

# Create test database
db-test:
	sqlite3 test.db "CREATE TABLE test (id INTEGER);"

# Show coverage gaps (requires htmlcov)
coverage-gaps:
	@grep -r "class="' htmlcov/index.html | grep -v "class=\"pln\"" | head -20

# Install pre-commit hooks
precommit-install:
	pip install pre-commit
	pre-commit install

.DEFAULT_GOAL := help
