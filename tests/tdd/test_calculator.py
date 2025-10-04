import pytest
from app.calculator import Calculator


class TestCalculator:
    """TDD unit tests for Calculator class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.calculator = Calculator()

    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        result = self.calculator.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        result = self.calculator.add(-5, -3)
        assert result == -8

    def test_add_zero(self):
        """Test adding zero"""
        result = self.calculator.add(5, 0)
        assert result == 5

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        result = self.calculator.subtract(10, 4)
        assert result == 6

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        result = self.calculator.subtract(-5, -3)
        assert result == -2

    def test_subtract_to_negative(self):
        """Test subtraction resulting in negative"""
        result = self.calculator.subtract(3, 10)
        assert result == -7

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        result = self.calculator.multiply(3, 4)
        assert result == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero"""
        result = self.calculator.multiply(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers"""
        result = self.calculator.multiply(-3, -4)
        assert result == 12

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        result = self.calculator.divide(10, 2)
        assert result == 5

    def test_divide_with_remainder(self):
        """Test division with remainder"""
        result = self.calculator.divide(7, 2)
        assert result == 3.5


    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        result = self.calculator.divide(-10, -2)
        assert result == 5
