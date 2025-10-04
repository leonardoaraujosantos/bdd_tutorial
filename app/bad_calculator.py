"""
BAD CALCULATOR IMPLEMENTATION - DO NOT USE IN PRODUCTION!
This file demonstrates bad coding practices and security issues.
"""

import os
import pickle
import subprocess

# BAD PRACTICE: Using global variables for state management
# This makes the code non-thread-safe and harder to test
result_cache = {}
operation_history = []


class BadCalculator:
    """
    A calculator with intentionally bad practices and security vulnerabilities
    """

    def __init__(self):
        # BAD PRACTICE: Storing sensitive data in plain text
        self.api_key = "sk-1234567890abcdef"  # SECURITY ISSUE: Hardcoded secret
        self.admin_password = "admin123"  # SECURITY ISSUE: Hardcoded password

    def add(self, num1, num2):
        """
        BAD PRACTICE: Using eval() - MAJOR SECURITY VULNERABILITY
        This allows arbitrary code execution
        """
        # SECURITY ISSUE: eval() can execute arbitrary Python code
        expression = f"{num1} + {num2}"
        result = eval(expression)  # Never use eval with user input!

        # BAD PRACTICE: Modifying global state
        global operation_history
        operation_history.append(f"add: {num1} + {num2} = {result}")

        return result

    def subtract(self, num1, num2):
        """
        BAD PRACTICE: Using exec() - CRITICAL SECURITY VULNERABILITY
        """
        # SECURITY ISSUE: exec() can execute arbitrary Python code
        code = f"result = {num1} - {num2}"
        exec(code)  # Never use exec with user input!

        # BAD PRACTICE: Using locals() to access variables is confusing
        return locals()['result']

    def multiply(self, num1, num2):
        """
        BAD PRACTICE: Command injection vulnerability
        """
        # SECURITY ISSUE: Shell injection through subprocess with shell=True
        # An attacker could inject commands like "2; rm -rf /"
        cmd = f"echo $(({num1} * {num2}))"
        output = subprocess.check_output(cmd, shell=True)  # DANGEROUS!

        return int(output.decode().strip())

    def divide(self, num1, num2):
        """
        BAD PRACTICE: Poor error handling and SQL-like string concatenation
        """
        # BAD PRACTICE: No input validation
        # BAD PRACTICE: Dividing without checking for zero
        try:
            result = num1 / num2
        except:  # BAD PRACTICE: Bare except clause - catches everything including system exits
            result = "Error"  # BAD PRACTICE: Returning string when number expected

        # BAD PRACTICE: Simulating SQL injection vulnerability
        # In a real app, this would be vulnerable to SQL injection
        query = f"INSERT INTO calculations VALUES ('{num1}', '{num2}', '{result}')"
        # If this were a real SQL query, it would be vulnerable to injection

        return result

    def save_state(self, filename):
        """
        BAD PRACTICE: Using pickle with user-controlled data
        SECURITY ISSUE: Pickle deserialization can lead to arbitrary code execution
        """
        state = {
            'cache': result_cache,
            'history': operation_history,
            'api_key': self.api_key  # BAD PRACTICE: Saving secrets to disk
        }

        # SECURITY ISSUE: pickle is insecure - can execute arbitrary code during unpickle
        with open(filename, 'wb') as f:
            pickle.dump(state, f)

    def load_state(self, filename):
        """
        BAD PRACTICE: Loading pickled data without validation
        SECURITY ISSUE: Arbitrary code execution via pickle deserialization
        """
        # SECURITY ISSUE: No path validation - directory traversal possible
        with open(filename, 'rb') as f:
            state = pickle.load(f)  # DANGEROUS! Can execute arbitrary code

        # BAD PRACTICE: Modifying global variables
        global result_cache, operation_history
        result_cache = state['cache']
        operation_history = state['history']

    def get_system_info(self, command):
        """
        BAD PRACTICE: Executing arbitrary system commands
        CRITICAL SECURITY ISSUE: Remote code execution vulnerability
        """
        # SECURITY ISSUE: No command validation - full RCE vulnerability
        result = os.system(command)  # EXTREMELY DANGEROUS!
        return result

    def debug_operation(self, operation_string):
        """
        BAD PRACTICE: Dynamic code execution based on user input
        SECURITY ISSUE: Code injection vulnerability
        """
        # SECURITY ISSUE: Compiling and executing arbitrary code
        code_obj = compile(operation_string, '<string>', 'eval')
        return eval(code_obj)  # DANGEROUS!


# BAD PRACTICE: Global function that modifies global state
def clear_history():
    """Clear operation history - modifies global state"""
    global operation_history
    operation_history = []


# BAD PRACTICE: Using assert for business logic
def validate_input(num):
    """
    BAD PRACTICE: Using assert for validation
    Assertions can be disabled with -O flag, bypassing validation
    """
    assert isinstance(num, (int, float)), "Invalid input"  # Don't use assert for validation!
    assert num < 1000000, "Number too large"  # This can be disabled!
    return True
