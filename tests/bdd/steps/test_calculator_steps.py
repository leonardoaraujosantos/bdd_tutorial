import pytest
from pytest_bdd import scenarios, given, when, then, parsers


# Load scenarios from the feature file
scenarios('../features/calculator.feature')


@given('the calculator is running')
def calculator_is_running(client, context):
    """Verify the calculator API is running"""
    response = client.get("/")
    assert response.status_code == 200
    context['client'] = client


@when(parsers.parse('I add {num1:d} and {num2:d}'))
def add_two_numbers(context, num1, num2):
    """Perform addition operation"""
    response = context['client'].post("/add", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I subtract {num1:d} and {num2:d}'))
def subtract_two_numbers(context, num1, num2):
    """Perform subtraction operation"""
    response = context['client'].post("/subtract", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I multiply {num1:d} and {num2:d}'))
def multiply_two_numbers(context, num1, num2):
    """Perform multiplication operation"""
    response = context['client'].post("/multiply", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


@when(parsers.parse('I divide {num1:d} and {num2:d}'))
def divide_two_numbers(context, num1, num2):
    """Perform division operation"""
    response = context['client'].post("/divide", json={"num1": num1, "num2": num2})
    context['response'] = response
    context['result'] = response.json().get('result')


#@when(parsers.parse('I attempt to divide {num1:d} by {num2:d}'))
#def attempt_divide_by_zero(context, num1, num2):
#    """Attempt division that may cause an error"""
#    response = context['client'].post("/divide", json={"num1": num1, "num2": num2})
#    context['response'] = response


@then(parsers.parse('the result should be {expected:d}'))
def verify_result(context, expected):
    """Verify the result matches expected value"""
    assert context['response'].status_code == 200
    assert context['result'] == expected


#@then('I should receive an error message')
#def verify_error_message(context):
#    """Verify that an error was returned"""
#    assert context['response'].status_code == 400
#    assert 'detail' in context['response'].json()
