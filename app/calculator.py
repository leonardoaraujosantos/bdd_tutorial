class Calculator:
    """Calculator service for performing arithmetic operations"""

    @staticmethod
    def add(num1: float, num2: float) -> float:
        """Add two numbers"""
        return num1 + num2

    @staticmethod
    def subtract(num1: float, num2: float) -> float:
        """Subtract num2 from num1"""
        return num1 - num2

    @staticmethod
    def multiply(num1: float, num2: float) -> float:
        """Multiply two numbers"""
        return num1 * num2

    @staticmethod
    def divide(num1: float, num2: float) -> float:
        """Divide num1 by num2"""
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
