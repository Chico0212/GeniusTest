import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from calculator.cli import app, state
from calculator import Calculator

class TestCalculatorCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        state["calc"] = Calculator()

    def test_add(self):
        result = self.runner.invoke(app, ["add", "2", "3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 5.0", result.output)

    def test_subtract(self):
        result = self.runner.invoke(app, ["subtract", "5", "2"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 3.0", result.output)

    def test_multiply(self):
        result = self.runner.invoke(app, ["multiply", "4", "2"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 8.0", result.output)

    def test_divide_success(self):
        result = self.runner.invoke(app, ["divide", "10", "2"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 5.0", result.output)

    def test_divide_by_zero(self):
        result = self.runner.invoke(app, ["divide", "10", "0"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Cannot divide by zero", result.output)

    def test_power(self):
        result = self.runner.invoke(app, ["power", "2", "3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 8.0", result.output)

    def test_history_empty(self):
        result = self.runner.invoke(app, ["history"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No calculations in history", result.output)

    def test_history_with_calculations(self):
        self.runner.invoke(app, ["add", "1", "2"])
        self.runner.invoke(app, ["subtract", "5", "3"])
        result = self.runner.invoke(app, ["history"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Calculation History:", result.output)
        self.assertIn("1.0 + 2.0 = 3.0", result.output)
        self.assertIn("5.0 - 3.0 = 2.0", result.output)

    def test_clear_history(self):
        self.runner.invoke(app, ["add", "1", "2"])
        result = self.runner.invoke(app, ["clear"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("History cleared", result.output)
        result = self.runner.invoke(app, ["history"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No calculations in history", result.output)
        
    def test_multiple_operations(self):
        self.runner.invoke(app, ["add", "5", "5"])
        self.runner.invoke(app, ["multiply", "2", "5"])
        result = self.runner.invoke(app, ["history"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("5.0 + 5.0 = 10.0", result.output)
        self.assertIn("2.0 * 5.0 = 10.0", result.output)
        
    def test_large_numbers(self):
        result = self.runner.invoke(app, ["multiply", "1000000", "2000000"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 2000000000000.0", result.output)
        
    def test_negative_numbers(self):
        result = self.runner.invoke(app, ["add", "--", "-5", "-3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: -8.0", result.output)

    def test_subtract_negative_numbers(self):
        result = self.runner.invoke(app, ["subtract", "--", "-5", "-3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: -2.0", result.output)

    def test_multiply_negative_numbers(self):
        result = self.runner.invoke(app, ["multiply", "--", "-4", "-2"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 8.0", result.output)

    def test_mixed_positive_negative(self):
        result = self.runner.invoke(app, ["add", "--", "5", "-3"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Result: 2.0", result.output)

if __name__ == '__main__':
    unittest.main()