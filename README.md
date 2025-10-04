# Calculator API - BDD/TDD Tutorial

A demonstration project showing the difference between good and bad code, and how BDD tests can pass even with terrible implementations.

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

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Good Implementation ✅
```bash
uvicorn app.main:app --reload
```

### Bad Implementation ❌ (DO NOT USE!)
```bash
uvicorn app.bad_main:app --reload
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

### Security Scan
```bash
semgrep --config=.semgrep.yml app/
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

## Testing Philosophy

```
Good Code → Easy Tests → High Confidence
Bad Code → Hard Tests → False Confidence (tests pass but code is dangerous!)
```

This project proves you need **multiple layers of quality assurance**:
- BDD (behavior correctness)
- TDD (implementation quality)
- Static analysis (security)
- Code review (design & maintainability)

## License

MIT - Educational purposes only. DO NOT use bad_calculator.py in production!
