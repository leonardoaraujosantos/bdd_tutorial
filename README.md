# Calculator API - BDD/TDD Tutorial

A comprehensive demonstration project showing the difference between good and bad code, and how BDD tests can pass even with terrible implementations. This project teaches the importance of using multiple quality assurance techniques: BDD, TDD, and static analysis tools like Semgrep.

## 📚 What is BDD, TDD, and Semgrep?

### Behavior-Driven Development (BDD)

**BDD** is a software development approach that focuses on the **behavior** of the application from the user's perspective.

- **What it is**: Write tests in plain language (Gherkin) that describe what the system should do
- **Focus**: External behavior and business requirements
- **Format**: Given-When-Then scenarios
- **Example**:
  ```gherkin
  Scenario: Add two numbers
    Given the calculator is running
    When I add 2 and 3
    Then the result should be 5
  ```
- **Limitation**: ⚠️ BDD only validates behavior, NOT code quality or security!

### Test-Driven Development (TDD)

**TDD** is a development practice where you write tests **before** writing the actual code.

- **What it is**: Write failing tests first, then write code to make them pass
- **Focus**: Implementation quality and code design
- **Process**:
  1. 🔴 Red - Write a failing test
  2. 🟢 Green - Write minimal code to pass
  3. 🔵 Refactor - Improve code quality
- **Benefits**:
  - Better code design
  - Higher test coverage
  - Easier to refactor
  - Exposes poor design early

### Semgrep - Static Analysis Security Tool

**Semgrep** is a fast, open-source static analysis tool that finds bugs and enforces code standards.

- **What it is**: Scans code for security vulnerabilities, bugs, and anti-patterns
- **How it works**: Uses pattern matching to find dangerous code
- **What it detects**:
  - Security vulnerabilities (SQL injection, XSS, code injection)
  - Hardcoded secrets and credentials
  - Dangerous functions (`eval()`, `exec()`, `pickle.load()`)
  - Code quality issues
- **Why it matters**: Catches what tests miss!

**Example Semgrep rule:**
```yaml
- id: dangerous-eval-usage
  pattern: eval(...)
  message: "Dangerous use of eval() - allows arbitrary code execution"
  severity: ERROR
```

## Project Structure

```
calculator-api/
├── app/
│   ├── main.py              # Good implementation ✅
│   ├── calculator.py        # Good calculator logic ✅
│   ├── models.py            # Pydantic models
│   ├── bad_main.py          # BAD implementation ❌
│   └── bad_calculator.py    # BAD calculator with security issues ❌
├── tests/
│   ├── bdd/
│   │   ├── features/
│   │   │   ├── calculator.feature      # BDD scenarios for good code
│   │   │   └── bad_calculator.feature  # BDD scenarios (PASS despite bad code!)
│   │   └── steps/
│   │       ├── test_calculator_steps.py
│   │       └── test_bad_calculator_steps.py
│   └── tdd/
│       ├── test_calculator.py      # Easy to write, clean tests ✅
│       ├── test_api.py
│       └── test_bad_calculator.py  # Hard to write, complex tests ❌
└── .semgrep.yml             # Security rules to catch bad code
```

## Key Learnings

### 1. BDD Can Pass with Bad Code! ⚠️

The **bad_calculator.py** demonstrates that:
- ✅ BDD tests **PASS** because behavior is correct
- ❌ Implementation has **critical security vulnerabilities**
- ❌ Code uses `eval()`, `exec()`, shell injection, and more

**Lesson**: BDD validates behavior, NOT code quality or security!

### 2. Bad Code Makes Testing Harder

Compare the tests:
- **Good code** (`test_calculator.py`): Clean, simple, isolated tests
- **Bad code** (`test_bad_calculator.py`):
  - Requires managing global state
  - Can't safely test security vulnerabilities
  - Tests interfere with each other
  - Many tests must be skipped due to danger

**Lesson**: If testing is hard, your code is probably bad!

### 3. Security Issues in Bad Code

`bad_calculator.py` contains intentional vulnerabilities:

| Issue | Severity | Location |
|-------|----------|----------|
| `eval()` code injection | 🔴 CRITICAL | `add()` method |
| `exec()` code execution | 🔴 CRITICAL | `subtract()` method |
| Shell injection | 🔴 CRITICAL | `multiply()` method |
| Pickle deserialization | 🔴 CRITICAL | `load_state()` method |
| RCE via `os.system()` | 🔴 CRITICAL | `get_system_info()` |
| Hardcoded secrets | 🟡 HIGH | `__init__()` |
| SQL injection pattern | 🔴 CRITICAL | `divide()` method |
| Bare except clauses | 🟡 MEDIUM | `divide()` method |
| Assert for validation | 🟡 MEDIUM | `validate_input()` |
| Global state | 🟡 MEDIUM | Throughout |

### 4. Semgrep Catches What BDD Misses

Run Semgrep to detect security issues:

```bash
pip install semgrep
semgrep --config=.semgrep.yml app/
```

Semgrep will detect:
- Code injection vulnerabilities
- Shell injection
- Hardcoded secrets
- Insecure deserialization
- And more!

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Run the good calculator API
docker-compose up calculator-api

# Access at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

**With Sentry monitoring:**
```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your Sentry DSN
# SENTRY_DSN=https://your-key@o0.ingest.sentry.io/0

# Run with Sentry enabled
docker-compose up calculator-api
```

To run the bad calculator (for educational purposes only):
```bash
# Run with the 'demo' profile
docker-compose --profile demo up bad-calculator-api

# Access at: http://localhost:8001
```

### Option 2: Local Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure Sentry
cp .env.example .env
# Edit .env and add your Sentry DSN

# Run the good implementation
export SENTRY_DSN="your-sentry-dsn"  # Optional
uvicorn app.main:app --reload

# Access at: http://localhost:8000
```

## 🐳 Docker Commands

```bash
# Build the image
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Run tests in container
docker-compose run calculator-api pytest
```

## Running Tests

### All Tests
```bash
pytest
```

### TDD Tests Only
```bash
pytest tests/tdd/
```

### BDD Tests Only
```bash
pytest tests/bdd/
```

### With Coverage
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Security Scan with Semgrep

```bash
# Install Semgrep
pip install semgrep

# Run security scan
semgrep --config=.semgrep.yml app/

# Output results to JSON
semgrep --config=.semgrep.yml --json app/ > security-report.json

# Scan only bad code to see vulnerabilities
semgrep --config=.semgrep.yml app/bad_calculator.py
```

**Expected output for bad_calculator.py:**
```
Findings:
  app/bad_calculator.py
     dangerous-eval-usage
        Dangerous use of eval() - allows arbitrary code execution

     dangerous-exec-usage
        Dangerous use of exec() - allows arbitrary code execution

     shell-injection-subprocess
        Shell injection vulnerability - subprocess with shell=True

     [... and more security issues]
```

## CI/CD Pipeline

The GitHub Actions workflow runs:
1. ✅ TDD tests
2. ✅ BDD tests
3. ✅ Coverage reporting
4. ✅ Semgrep security scan

**Important**: Notice that BDD tests for bad_calculator **PASS** in CI, but Semgrep **FAILS** with security errors!

## Key Takeaways

1. **BDD is not enough** - It validates behavior, not implementation quality
2. **Bad code is hard to test** - Difficulty in testing indicates poor code quality
3. **Use multiple tools**:
   - BDD for behavior validation
   - TDD for implementation quality
   - Semgrep/Bandit for security
   - Code review for overall quality
4. **Passing tests ≠ Good code** - You need comprehensive quality checks

## Good vs Bad Code Comparison

### Good Calculator (`calculator.py`)
- ✅ Pure functions, no side effects
- ✅ No global state
- ✅ Proper error handling with exceptions
- ✅ Type safe
- ✅ Easy to test
- ✅ No security vulnerabilities

### Bad Calculator (`bad_calculator.py`)
- ❌ Uses `eval()` and `exec()` - code injection
- ❌ Global state - not thread-safe
- ❌ Shell injection vulnerabilities
- ❌ Hardcoded secrets
- ❌ Insecure pickle deserialization
- ❌ Poor error handling
- ❌ Hard to test safely

## 🧪 How to Use This Project for Learning

### Step 1: Run BDD Tests
```bash
pytest tests/bdd/ -v
```
**Observe**: Both good and bad calculator BDD tests PASS! ✅

### Step 2: Run TDD Tests
```bash
pytest tests/tdd/ -v
```
**Observe**: Notice how tests for bad code are harder to write and some are skipped

### Step 3: Run Semgrep
```bash
semgrep --config=.semgrep.yml app/
```
**Observe**: Semgrep finds critical vulnerabilities in bad_calculator.py! 🚨

### Step 4: Compare Code Quality
- Open `app/calculator.py` (good code) - clean and simple
- Open `app/bad_calculator.py` (bad code) - full of vulnerabilities

### Key Lesson
**BDD tests pass for both!** But only Semgrep and careful TDD expose the bad code.

## 📊 Testing Philosophy

```
Good Code → Easy Tests → High Confidence ✅
Bad Code → Hard Tests → False Confidence ❌ (tests pass but code is dangerous!)
```

### The Three Pillars of Quality

1. **BDD** 🎭 - Validates external behavior
   - ✅ Ensures features work as expected
   - ❌ Doesn't catch implementation flaws

2. **TDD** 🔬 - Validates internal quality
   - ✅ Exposes design problems
   - ✅ Hard to test = bad design
   - ❌ Can't catch all security issues

3. **Static Analysis** 🔒 - Validates security
   - ✅ Finds vulnerabilities
   - ✅ Detects dangerous patterns
   - ✅ Catches what tests miss

**Conclusion**: You need **ALL THREE** for production-ready code!

## 🔍 Sentry Integration - Error Monitoring & Performance

This project includes full Sentry integration for:
- **Error Monitoring**: Automatically track all exceptions
- **Performance Monitoring**: Track request performance and database queries
- **Profiling**: CPU profiling for performance optimization
- **Logging**: Send application logs to Sentry

### Setup Sentry

1. **Create a Sentry Account**: Go to [sentry.io](https://sentry.io) and create a free account
2. **Create a Project**: Create a new Python/FastAPI project
3. **Get your DSN**: Copy your project's DSN (Data Source Name)
4. **Configure the application**:

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Sentry DSN
SENTRY_DSN=https://your-key@o0.ingest.sentry.io/0
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_PROFILES_SAMPLE_RATE=1.0
```

### Test Sentry Integration

#### 1. Test Error Tracking
```bash
# Trigger an intentional error
curl http://localhost:8000/sentry-debug
```
This will create a ZeroDivisionError that gets sent to Sentry. Check your Sentry dashboard to see the error!

#### 2. Test Logging
```bash
# Send test logs to Sentry
curl http://localhost:8000/sentry-log-test
```
This will send various log levels (info, warning, error) to Sentry. Check the "Logs" section in Sentry.

#### 3. Test Performance Monitoring
```bash
# Make normal API requests
curl -X POST "http://localhost:8000/add" \
  -H "Content-Type: application/json" \
  -d '{"num1": 5, "num2": 3}'
```
Check the "Performance" section in Sentry to see transaction traces!

### What Gets Sent to Sentry

✅ **Errors**: All unhandled exceptions
✅ **Performance**: Request duration, database queries
✅ **Logs**: Application logs (info, warning, error)
✅ **Context**: Request headers, user data, environment info
✅ **Stack Traces**: Full stack traces with local variables

### Sentry Configuration Options

The SDK is configured with:
- `send_default_pii=True`: Includes request headers and IP addresses
- `enable_logs=True`: Sends Python logs to Sentry
- `traces_sample_rate=1.0`: Captures 100% of transactions (reduce in production)
- `profile_session_sample_rate=1.0`: Profiles 100% of sessions
- `profile_lifecycle="trace"`: Auto-profile during transactions

### Sentry in Production

For production, adjust sample rates to reduce data volume:

```python
traces_sample_rate=0.1  # 10% of transactions
profile_session_sample_rate=0.1  # 10% of sessions
```

## 📖 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

#### Good Calculator API (Port 8000)
- `POST /add` - Add two numbers
- `POST /subtract` - Subtract two numbers
- `POST /multiply` - Multiply two numbers
- `POST /divide` - Divide two numbers (with error handling)
- `GET /sentry-debug` - Test Sentry error tracking
- `GET /sentry-log-test` - Test Sentry logging

#### Example Request
```bash
curl -X POST "http://localhost:8000/add" \
  -H "Content-Type: application/json" \
  -d '{"num1": 5, "num2": 3}'
```

#### Example Response
```json
{
  "result": 8.0,
  "operation": "addition"
}
```

#### Test Division by Zero (Error Tracking)
```bash
curl -X POST "http://localhost:8000/divide" \
  -H "Content-Type: application/json" \
  -d '{"num1": 10, "num2": 0}'
```
This error will be logged to Sentry with full context!

## 🎯 Project Goals

This project demonstrates:
1. ✅ How to write BDD tests using pytest-bdd and Gherkin
2. ✅ How to write TDD tests for FastAPI applications
3. ✅ How BDD can pass with terrible code quality
4. ✅ How bad code makes testing harder
5. ✅ How to use Semgrep to find security vulnerabilities
6. ✅ How to integrate Sentry for error monitoring and performance tracking
7. ✅ Why you need multiple quality assurance techniques

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more bad code examples
- Create additional Semgrep rules
- Improve documentation
- Add more test scenarios

## 📝 License

MIT - Educational purposes only. **DO NOT use bad_calculator.py in production!**

## ⚠️ Security Warning

The `bad_calculator.py` file contains **intentional security vulnerabilities** for educational purposes:
- Remote Code Execution (RCE)
- SQL Injection patterns
- Command Injection
- Hardcoded secrets
- Insecure deserialization

**Never deploy this code to production!** It serves only as a teaching tool to demonstrate what NOT to do.
