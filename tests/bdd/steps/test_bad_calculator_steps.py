"""
BDD Step Definitions for Bad Calculator

IMPORTANT LESSON: These BDD tests PASS even though the code is terrible!

This demonstrates that:
1. BDD validates behavior, not implementation quality
2. You need additional tools (Semgrep, SonarQube, code review) to catch bad code
3. Passing tests don't guarantee secure or maintainable code
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.bad_main import app


# Load scenarios from the bad calculator feature file
scenarios('../features/bad_calculator.feature')


@given('the bad calculator is running')
def bad_calculator_is_running(client, context):
    """
    Verify the bad calculator API is running
    The BDD test passes, but doesn't check for security issues!
    """
    response = client.get("/")
    assert response.status_code == 200
    context['client'] = client


@when(parsers.parse('I add {num1:d} and {num2:d} using bad calculator'))
def add_with_bad_calculator(context, num1, num2):
    """
    Perform addition using bad calculator

    BDD TEST LIMITATION: This test passes because the OUTPUT is correct,
    even though internally it uses eval() which is a MAJOR security vulnerability!

    The test doesn't know that eval("2 + 3") is dangerous.
    It only checks that the result is 5.
    """
    response = context['client'].post("/add", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I subtract {num1:d} and {num2:d} using bad calculator'))
def subtract_with_bad_calculator(context, num1, num2):
    """
    Perform subtraction using bad calculator

    BDD TEST LIMITATION: Passes even though it uses exec() internally!
    The test only validates the behavior, not the implementation.
    """
    response = context['client'].post("/subtract", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I multiply {num1:d} and {num2:d} using bad calculator'))
def multiply_with_bad_calculator(context, num1, num2):
    """
    Perform multiplication using bad calculator

    BDD TEST LIMITATION: Passes even with shell injection vulnerability!
    The test doesn't care that it's using subprocess.check_output with shell=True
    """
    response = context['client'].post("/multiply", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I divide {num1:d} and {num2:d} using bad calculator'))
def divide_with_bad_calculator(context, num1, num2):
    """
    Perform division using bad calculator

    BDD TEST LIMITATION: This scenario passes because we're not testing edge cases
    The poor error handling isn't exposed in this basic scenario
    """
    response = context['client'].post("/divide", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@then(parsers.parse('the bad calculator result should be {expected:d}'))
def verify_bad_calculator_result(context, expected):
    """
    Verify the result from bad calculator

    KEY INSIGHT: This assertion passes because the BEHAVIOR is correct,
    even though the IMPLEMENTATION is terrible!

    This is why you need:
    - Static analysis (Semgrep, Bandit)
    - Code review
    - Security scanning
    - TDD to expose implementation issues

    BDD alone is not enough!
    """
    assert context['response'].status_code == 200
    assert context['result'] == expected

    # The test passes here, completely unaware of:
    # - eval() code injection vulnerability
    # - exec() code execution vulnerability
    # - Shell injection vulnerability
    # - Hardcoded secrets
    # - Global state issues
    # - Poor error handling
