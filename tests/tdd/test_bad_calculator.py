"""
TDD Tests for Bad Calculator - Notice how testing bad code is harder!

These tests demonstrate:
1. Tests are harder to write due to global state
2. Tests can interfere with each other
3. Security vulnerabilities make tests unpredictable
4. Hard to mock/isolate components
"""

import pytest
import os
import tempfile
from app.bad_calculator import BadCalculator, clear_history, operation_history


class TestBadCalculator:
    """
    TDD tests for bad calculator - notice the complexity!
    """

    def setup_method(self):
        """
        PROBLEM: We have to clear global state before each test
        This is a sign of bad design - good code doesn't need this
        """
        self.calculator = BadCalculator()
        clear_history()  # Have to manage global state manually!

    def test_add_basic(self):
        """
        This test works, but internally uses dangerous eval()
        The test doesn't reveal the security vulnerability
        """
        result = self.calculator.add(2, 3)
        assert result == 5

    def test_add_modifies_global_state(self):
        """
        PROBLEM: Testing global state is a code smell
        Good code shouldn't require testing global state
        """
        self.calculator.add(2, 3)
        # BAD: We have to test global state
        assert len(operation_history) == 1
        assert "add: 2 + 3 = 5" in operation_history[0]

    def test_add_with_malicious_input_shows_vulnerability(self):
        """
        PROBLEM: This test exposes the eval() vulnerability
        An attacker could inject code through num1 or num2
        """
        # This is dangerous - eval will execute the code!
        # In a real scenario, this could delete files, steal data, etc.
        # We can't easily test this without actually running dangerous code
        pass  # Can't safely test this vulnerability!

    def test_subtract_basic(self):
        """Test basic subtraction - but uses dangerous exec()"""
        result = self.calculator.subtract(10, 4)
        assert result == 6

    def test_multiply_basic(self):
        """
        Test multiplication - but uses shell command
        PROBLEM: This test requires shell access and is slow
        """
        result = self.calculator.multiply(3, 4)
        assert result == 12

    @pytest.mark.skipif(os.name == 'nt', reason="Shell behavior differs on Windows")
    def test_multiply_shell_dependency(self):
        """
        PROBLEM: Tests depend on shell environment
        Good code shouldn't require shell access for math!
        """
        result = self.calculator.multiply(5, 5)
        assert result == 25

    def test_divide_basic(self):
        """Test division with proper inputs"""
        result = self.calculator.divide(10, 2)
        assert result == 5

    def test_divide_by_zero_bad_error_handling(self):
        """
        PROBLEM: The error handling is inconsistent
        Returns "Error" string instead of raising exception
        This makes type checking impossible
        """
        result = self.calculator.divide(10, 0)
        # BAD: We get a string instead of proper error handling
        assert result == "Error"
        # This is terrible because the return type is inconsistent!

    def test_save_and_load_state_security_issue(self):
        """
        PROBLEM: Using pickle is a security vulnerability
        This test works but the implementation is dangerous
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            temp_file = f.name

        try:
            # Add some operations
            self.calculator.add(1, 1)
            self.calculator.add(2, 2)

            # Save state - BAD: Saves secrets to disk!
            self.calculator.save_state(temp_file)

            # Clear and reload
            clear_history()
            assert len(operation_history) == 0

            # Load state - BAD: Pickle deserialization vulnerability!
            self.calculator.load_state(temp_file)

            # PROBLEM: We're testing that insecure functionality works
            assert len(operation_history) == 2

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_hardcoded_secrets_exposed(self):
        """
        PROBLEM: Hardcoded secrets in the code
        This test reveals the security issue
        """
        # BAD: API keys and passwords are hardcoded and exposed
        assert self.calculator.api_key == "sk-1234567890abcdef"
        assert self.calculator.admin_password == "admin123"
        # In real code, these should NEVER be hardcoded!

    @pytest.mark.skip(reason="Too dangerous to test - RCE vulnerability")
    def test_get_system_info_rce_vulnerability(self):
        """
        PROBLEM: Cannot safely test RCE vulnerability
        Testing this could actually harm the system!
        """
        # We can't test this without risking the system
        # This is a sign of extremely bad code
        pass

    @pytest.mark.skip(reason="Code injection vulnerability - too dangerous")
    def test_debug_operation_code_injection(self):
        """
        PROBLEM: Cannot safely test code injection
        Good code wouldn't have this vulnerability
        """
        # Can't test without actually injecting code
        pass

    def test_global_state_interference(self):
        """
        PROBLEM: Tests can interfere with each other due to global state
        This is why we need setup_method to clear state
        """
        # First calculator instance
        calc1 = BadCalculator()
        calc1.add(1, 1)

        # Second calculator instance - shares global state!
        calc2 = BadCalculator()
        calc2.add(2, 2)

        # BAD: Global state means both instances share history
        assert len(operation_history) == 2  # State from both instances!

    def test_validate_input_assert_vulnerability(self):
        """
        PROBLEM: Using assert for validation is wrong
        Assertions can be disabled with python -O flag
        """
        from app.bad_calculator import validate_input

        # This works in normal mode
        assert validate_input(5) == True

        # But if Python runs with -O flag, this would pass even with invalid input!
        # We can't easily test this vulnerability in unit tests


class TestBadCalculatorComplexity:
    """
    These tests show how bad code makes testing harder
    """

    def test_comment_on_testing_difficulty(self):
        """
        SUMMARY OF TESTING PROBLEMS WITH BAD CODE:

        1. GLOBAL STATE: Tests must manage global variables, causing:
           - Test interference
           - Need for complex setup/teardown
           - Non-deterministic failures

        2. SECURITY VULNERABILITIES: Can't safely test:
           - eval() code injection
           - exec() code execution
           - Shell command injection
           - Pickle deserialization
           - RCE vulnerabilities

        3. INCONSISTENT TYPES: Functions return different types:
           - Sometimes float, sometimes string
           - Makes type hints impossible
           - Breaks contract

        4. EXTERNAL DEPENDENCIES:
           - Requires shell access
           - File system operations
           - OS-specific behavior

        5. POOR ERROR HANDLING:
           - Bare except clauses
           - Silent failures
           - Returning error strings

        Good code is EASY to test. Bad code makes testing PAINFUL.
        This is a great indicator of code quality!
        """
        assert True  # This is a documentation test
