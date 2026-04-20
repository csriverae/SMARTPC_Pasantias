# 📋 Testing Guide for MesaPass Backend

## Table of Contents
1. [Quick Start](#quick-start)
2. [Test Structure](#test-structure)
3. [Running Tests](#running-tests)
4. [Coverage Reports](#coverage-reports)
5. [Security Testing](#security-testing)
6. [SonarQube Integration](#sonarqube-integration)
7. [CI/CD Integration](#cicd-integration)

---

## ⚡ Quick Start

### 1. Install Test Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio faker httpx
pip install bandit safety pylint
pip install sonar-scanner
```

### 2. Run Default Test Suite

```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

# Or use the test runner
python run_tests.py --all
```

### 3. View Coverage Report

```bash
# Open HTML report
# Windows:
start htmlcov/index.html

# macOS:
open htmlcov/index.html

# Linux:
xdg-open htmlcov/index.html
```

---

## 📁 Test Structure

```
tests/
├── conftest.py                 # Shared fixtures and configuration
├── unit/                       # Unit tests
│   ├── test_auth.py           # Authentication tests
│   ├── test_users.py          # User management tests
│   └── test_services.py       # Service layer tests
├── integration/                # Integration tests
│   ├── test_api_flow.py       # Complete API workflows
│   ├── test_multitenant.py    # Multi-tenant scenarios
│   └── test_database.py       # Database integration
└── security/                   # Security tests
    ├── test_security.py       # Security & authorization
    └── test_vulnerabilities.py # Known vulnerabilities
```

---

## 🚀 Running Tests

### Run All Tests

```bash
# Basic: Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# With markers (by type)
pytest tests/ -m "not slow"
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v -m unit

# Integration tests only
pytest tests/integration/ -v -m integration

# Security tests only
pytest tests/security/ -v -m security

# Skip security tests
pytest tests/ -v -m "not security"
```

### Run Specific Test File

```bash
pytest tests/unit/test_auth.py -v
```

### Run Specific Test

```bash
pytest tests/unit/test_auth.py::TestPasswordHashing::test_hash_password_creates_hash -v
```

### Run Tests in Parallel (faster)

```bash
pip install pytest-xdist
pytest tests/ -v -n auto  # Run on all CPU cores
```

---

## 📊 Coverage Reports

### Generate HTML Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html
```

**Output**: `htmlcov/index.html` - Interactive coverage report

### Terminal Coverage Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

**Shows**: File-by-file coverage with missing lines

### XML Coverage Report (for CI/CD)

```bash
pytest tests/ --cov=app --cov-report=xml
```

**Output**: `coverage.xml` - For SonarQube integration

### Coverage Configuration

Edit `pytest.ini` to adjust:
- `--cov-fail-under=70` - Minimum coverage threshold
- `exclude_lines` - Lines to exclude from coverage
- `omit` - Files/directories to skip

---

## 🔐 Security Testing

### 1. Bandit - Static Security Analysis

```bash
# Scan for security issues
bandit -r app/ -v

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json

# Only high severity
bandit -r app/ -ll

# With specific plugin
bandit -r app/ --plugins flask_sql_injection
```

### 2. Safety - Dependency Vulnerability Check

```bash
# Check for known CVE vulnerabilities in dependencies
safety check

# Generate JSON report
safety check --json > safety-report.json

# Only critical
safety check --critical
```

### 3. OWASP Dependency Check (Optional)

```bash
pip install dependency-check

# Scan dependencies
dependency-check --project "MesaPass" --scan .
```

### 4. Manual Security Tests

```bash
# Run only security test suite
pytest tests/security/ -v

# Includes tests for:
# - SQL Injection prevention
# - Authentication bypass
# - Password security
# - CSRF protection
# - Rate limiting
```

---

## 📈 Code Quality Analysis with Pylint

```bash
# Full analysis
pylint app/

# Generate report
pylint app/ --output-format=json > pylint-report.json

# Only critical messages
pylint app/ --disable=all --enable=C,E

# With configuration file
pylint app/ --rcfile=.pylintrc
```

---

## 🔬 SonarQube Integration

### Prerequisites

```bash
# Install SonarQube Scanner
# Windows (Chocolatey):
choco install sonar-scanner

# macOS (Homebrew):
brew install sonar-scanner

# Or manually download from:
# https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
```

### Step 1: Setup Coverage Report

```bash
# Generate coverage.xml
pytest tests/ --cov=app --cov-report=xml
```

### Step 2: Configure SonarQube

Edit `sonar-project.properties` and set:

```properties
sonar.projectKey=mesapass-backend
sonar.projectName=MesaPass Backend
sonar.projectVersion=1.0
sonar.host.url=https://your-sonarqube-server.com
sonar.login=your-sonarqube-token
```

### Step 3: Run Analysis

```bash
# Local analysis
sonar-scanner

# Or specify parameters
sonar-scanner \
  -Dsonar.projectKey=mesapass-backend \
  -Dsonar.sources=app \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqa_1234567890abcdef1234567890abcdef
```

### Step 4: View Results

Open SonarQube dashboard:
- URL: `http://your-sonarqube-server/dashboard`
- Project: `mesapass-backend`

### SonarQube Metrics

- **Code Smells**: Maintainability issues
- **Bugs**: Code defects
- **Vulnerabilities**: Security issues
- **Duplications**: Code duplication percentage
- **Coverage**: Test code coverage
- **Technical Debt**: Time to fix issues

---

## 🔄 CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests & Security Scan

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov bandit safety
      
      - name: Run tests
        run: |
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Run Bandit
        run: bandit -r app/ -f json -o bandit-report.json || true
      
      - name: Run Safety
        run: safety check --json > safety-report.json || true
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          files: ./coverage.xml
```

### GitLab CI Example

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - security
  - quality

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest tests/ --cov=app --cov-report=xml
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

security:
  stage: security
  script:
    - pip install bandit safety
    - bandit -r app/
    - safety check

sonarqube:
  stage: quality
  script:
    - pip install pytest pytest-cov
    - pytest tests/ --cov=app --cov-report=xml
    - sonar-scanner
```

---

## 📋 Complete Test Commands Reference

```bash
# ========== QUICK COMMANDS ==========

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific category
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/security/ -v

# Run test runner script
python run_tests.py --all
python run_tests.py --coverage
python run_tests.py --security
python run_tests.py --full  # All tests + security checks + sonar


# ========== SECURITY ==========

# Run all security checks
python run_tests.py --full

# Individual security tools
bandit -r app/ -v
safety check
pylint app/


# ========== COVERAGE ==========

# Generate coverage reports
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Set minimum coverage requirement
pytest tests/ --cov=app --cov-fail-under=80


# ========== SONARQUBE ==========

# Generate SonarQube compatible reports
pytest tests/ --cov=app --cov-report=xml
bandit -r app/ -f json -o bandit-report.json

# Run SonarQube analysis
sonar-scanner


# ========== DEBUGGING ==========

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Fail after N failures
pytest tests/ --maxfail=3

# Show local variables on failure
pytest tests/ -l

# Full traceback
pytest tests/ --tb=long
```

---

## ✅ Testing Best Practices

### 1. **Test Organization**
- Keep tests close to code
- Use descriptive names: `test_<feature>_<scenario>`
- Group related tests in classes

### 2. **Fixtures**
- Use `conftest.py` for shared fixtures
- Keep fixtures focused and reusable
- Document complex fixtures

### 3. **Assertions**
```python
# Good
assert response.status_code == 200
assert "error" not in response.text

# Avoid
assert response
```

### 4. **Mocking**
```python
from unittest.mock import patch

# Mock external service
@patch('app.services.external_api.call')
def test_with_mock(mock_call):
    mock_call.return_value = {"status": "ok"}
    # Test code
```

### 5. **Coverage Goals**
- Aim for **80%+ coverage** minimum
- 100% for critical paths (auth, payments)
- Use coverage report to find gaps

---

## 🏆 Testing Checklist

- [ ] All tests passing locally
- [ ] Coverage above 70%
- [ ] No security vulnerabilities (Bandit, Safety)
- [ ] Code quality passing (Pylint)
- [ ] SonarQube analysis reviewed
- [ ] CI/CD pipeline green
- [ ] Load tests passed (if applicable)
- [ ] Performance acceptable

---

## 📞 Support

For issues or questions:
1. Check test logs: `pytest -v -s`
2. Enable debug logging: `pytest --log-cli-level=DEBUG`
3. Review SonarQube dashboard for detailed metrics
4. Check `htmlcov/index.html` for coverage gaps

