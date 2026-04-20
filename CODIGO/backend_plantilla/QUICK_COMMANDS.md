# 🎯 Quick Test Commands Reference

## Installation

```bash
# Navigate to project
cd starter-kit/starter-kit

# Activate virtual environment
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate.ps1         # Windows PowerShell

# Install test dependencies
pip install -r requirements-dev.txt
```

---

## Running Tests

### Basic Test Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run tests and stop on first failure
pytest tests/ -x

# Run tests with 3 retries
pytest tests/ --maxfail=3

# Run tests in parallel (faster)
pytest tests/ -n auto
```

### By Category

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Security tests only
pytest tests/security/ -v

# All except security (if needed)
pytest tests/ -m "not security" -v
```

### Specific Tests

```bash
# Run specific file
pytest tests/unit/test_auth.py -v

# Run specific test class
pytest tests/unit/test_auth.py::TestPasswordHashing -v

# Run specific test
pytest tests/unit/test_auth.py::TestPasswordHashing::test_hash_password_creates_hash -v

# Run tests matching pattern
pytest tests/ -k "password" -v
```

### With Debug Output

```bash
# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Full traceback
pytest tests/ --tb=long
```

---

## Coverage Reports

### Generate Reports

```bash
# HTML Report (recommended)
pytest tests/ --cov=app --cov-report=html

# Terminal report
pytest tests/ --cov=app --cov-report=term-missing

# XML report (for SonarQube/CI)
pytest tests/ --cov=app --cov-report=xml

# JSON report
pytest tests/ --cov=app --cov-report=json

# Enforce minimum coverage (70%)
pytest tests/ --cov=app --cov-fail-under=70
```

### View Coverage Report

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows PowerShell
Start-Process htmlcov\index.html

# Windows CMD
start htmlcov\index.html
```

---

## Security Testing

### Bandit (Static Security Analysis)

```bash
# Scan all files
bandit -r app/ -v

# High/Critical only
bandit -r app/ -ll

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json

# Generate HTML report
bandit -r app/ -f html -o bandit-report.html
```

### Safety (Dependency Vulnerabilities)

```bash
# Check dependencies
safety check

# Check critical only
safety check --critical

# Generate JSON report
safety check --json > safety-report.json
```

### Pylint (Code Quality)

```bash
# Full analysis
pylint app/

# Only errors and critical
pylint app/ -d R,W

# JSON report
pylint app/ --output-format=json > pylint-report.json

# With config file
pylint app/ --rcfile=.pylintrc
```

---

## SonarQube Analysis

### Prerequisites

```bash
# Install SonarScanner
# macOS:
brew install sonar-scanner

# Windows (Chocolatey):
choco install sonar-scanner

# Or download manually from:
# https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
```

### Run Analysis

```bash
# Simple (uses sonar-project.properties)
sonar-scanner

# With parameters
sonar-scanner \
  -Dsonar.projectKey=mesapass \
  -Dsonar.sources=app \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN

# With coverage
pytest tests/ --cov=app --cov-report=xml
sonar-scanner -Dsonar.python.coverage.reportPaths=coverage.xml
```

### Full Workflow

```bash
# 1. Generate coverage
pytest tests/ --cov=app --cov-report=xml

# 2. Run security scans
bandit -r app/ -f json -o bandit-report.json
safety check --json > safety-report.json

# 3. Run SonarQube
sonar-scanner
```

---

## Complete Test Runner Script

```bash
# Run everything at once
python run_tests.py --full

# Options:
python run_tests.py --all          # All tests
python run_tests.py --unit         # Unit tests only
python run_tests.py --integration  # Integration tests only
python run_tests.py --security     # Security tests only
python run_tests.py --coverage     # With coverage
python run_tests.py --bandit       # Security scan
python run_tests.py --safety       # Dependency check
python run_tests.py --pylint       # Code quality
python run_tests.py --sonar        # SonarQube analysis
```

---

## CI/CD Integration

### GitHub Actions

```bash
# Triggers automatically on:
# - Push to main/develop
# - Pull requests to main/develop

# Runs:
# ✓ Unit tests
# ✓ Integration tests
# ✓ Security tests
# ✓ Coverage reports
# ✓ Bandit scan
# ✓ Safety check
# ✓ SonarQube analysis
```

View in GitHub: **Actions** tab

---

## Environment Setup

### Create Test Database

```bash
# Tests use SQLite in-memory by default
# No setup needed! Database automatically created and cleaned up

# For manual testing with PostgreSQL:
SQLALCHEMY_DATABASE_URL="postgresql://user:pass@localhost/test_db"
pytest tests/ -v
```

### Create Test User

Fixtures automatically create test users:
- **Email**: test@example.com
- **Password**: TestPassword123!
- **Admin**: admin@example.com
- **Password**: AdminPassword123!

---

## Common Issues & Solutions

### Import Errors

```bash
# Solution: Install dev dependencies
pip install -r requirements-dev.txt

# Or individual packages
pip install pytest pytest-cov bandit safety
```

### Database Locked

```bash
# Solution: Remove test database
rm test.db
pytest tests/ -v
```

### Coverage Too Low

```bash
# View uncovered lines
pytest tests/ --cov=app --cov-report=term-missing

# Open HTML report
open htmlcov/index.html
```

### Sonar Connection Error

```bash
# Check sonar-project.properties
cat sonar-project.properties

# Verify SonarQube is running
# Default: http://localhost:9000

# Check token is valid
echo $SONAR_TOKEN
```

---

## Test Strategy

| Type | Coverage | Purpose |
|------|----------|---------|
| **Unit** | 80%+ | Test individual functions/methods |
| **Integration** | 70%+ | Test API endpoints/workflows |
| **Security** | Critical paths | Test auth, authorization, vulnerabilities |
| **Coverage** | Overall 75%+ | Minimum coverage threshold |

---

## Metrics Target

| Metric | Target | Tool |
|--------|--------|------|
| Coverage | 75%+ | pytest-cov |
| Security Issues | 0 Critical | Bandit |
| CVE Vulnerabilities | 0 | Safety |
| Code Quality | A | Pylint |
| Duplications | <5% | SonarQube |

---

## Useful Aliases

Add to `.bashrc` or `.zshrc`:

```bash
alias test-all="pytest tests/ -v --cov=app --cov-report=html"
alias test-unit="pytest tests/unit/ -v"
alias test-sec="pytest tests/security/ -v"
alias test-cov="pytest tests/ --cov=app --cov-report=term-missing"
alias test-run="python run_tests.py"
alias sec-scan="bandit -r app/ && safety check"
```

Usage:

```bash
test-all
test-unit
test-sec
test-cov
sec-scan
```

---

## Documentation Links

- **Pytest**: https://docs.pytest.org/
- **Coverage.py**: https://coverage.readthedocs.io/
- **Bandit**: https://bandit.readthedocs.io/
- **Safety**: https://safety.readthedocs.io/
- **SonarQube**: https://docs.sonarqube.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

