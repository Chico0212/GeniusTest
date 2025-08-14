import unittest
from calculator import Calculator  # Supondo que o código esteja em calculator.py


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_add_positive_numbers(self):
        result = self.calculator.add(5, 3)
        self.assertEqual(result, 8)
        self.assertEqual(self.calculator.get_history(), ["5 + 3 = 8"])

    def test_add_negative_numbers(self):
        result = self.calculator.add(-5, -3)
        self.assertEqual(result, -8)
        self.assertEqual(self.calculator.get_history(), ["-5 + -3 = -8"])

    def test_add_mixed_numbers(self):
        result = self.calculator.add(5, -3)
        self.assertEqual(result, 2)
        self.assertEqual(self.calculator.get_history(), ["5 + -3 = 2"])

    def test_add_floats(self):
        result = self.calculator.add(2.5, 3.5)
        self.assertEqual(result, 6.0)
        self.assertEqual(self.calculator.get_history(), ["2.5 + 3.5 = 6.0"])

    def test_subtract_positive_numbers(self):
        result = self.calculator.subtract(5, 3)
        self.assertEqual(result, 2)
        self.assertEqual(self.calculator.get_history(), ["5 - 3 = 2"])

    def test_subtract_negative_numbers(self):
        result = self.calculator.subtract(-5, -3)
        self.assertEqual(result, -2)
        self.assertEqual(self.calculator.get_history(), ["-5 - -3 = -2"])

    def test_subtract_mixed_numbers(self):
        result = self.calculator.subtract(5, -3)
        self.assertEqual(result, 8)
        self.assertEqual(self.calculator.get_history(), ["5 - -3 = 8"])

    def test_subtract_floats(self):
        result = self.calculator.subtract(5.5, 2.5)
        self.assertEqual(result, 3.0)
        self.assertEqual(self.calculator.get_history(), ["5.5 - 2.5 = 3.0"])

    def test_multiply_positive_numbers(self):
        result = self.calculator.multiply(5, 3)
        self.assertEqual(result, 15)
        self.assertEqual(self.calculator.get_history(), ["5 * 3 = 15"])

    def test_multiply_negative_numbers(self):
        result = self.calculator.multiply(-5, -3)
        self.assertEqual(result, 15)
        self.assertEqual(self.calculator.get_history(), ["-5 * -3 = 15"])

    def test_multiply_mixed_numbers(self):
        result = self.calculator.multiply(5, -3)
        self.assertEqual(result, -15)
        self.assertEqual(self.calculator.get_history(), ["5 * -3 = -15"])

    def test_multiply_floats(self):
        result = self.calculator.multiply(2.5, 3.0)
        self.assertEqual(result, 7.5)
        self.assertEqual(self.calculator.get_history(), ["2.5 * 3.0 = 7.5"])

    def test_divide_positive_numbers(self):
        result = self.calculator.divide(6, 3)
        self.assertEqual(result, 2.0)
        self.assertEqual(self.calculator.get_history(), ["6 / 3 = 2.0"])

    def test_divide_negative_numbers(self):
        result = self.calculator.divide(-6, -3)
        self.assertEqual(result, 2.0)
        self.assertEqual(self.calculator.get_history(), ["-6 / -3 = 2.0"])

    def test_divide_mixed_numbers(self):
        result = self.calculator.divide(6, -3)
        self.assertEqual(result, -2.0)
        self.assertEqual(self.calculator.get_history(), ["6 / -3 = -2.0"])

    def test_divide_floats(self):
        result = self.calculator.divide(7.5, 2.5)
        self.assertEqual(result, 3.0)
        self.assertEqual(self.calculator.get_history(), ["7.5 / 2.5 = 3.0"])

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.divide(5, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")
        self.assertEqual(self.calculator.get_history(), []) # History deve estar inalterado

    def test_power_positive_numbers(self):
        result = self.calculator.power(2, 3)
        self.assertEqual(result, 8)
        self.assertEqual(self.calculator.get_history(), ["2 ^ 3 = 8"])

    def test_power_negative_numbers(self):
        result = self.calculator.power(-2, 3)
        self.assertEqual(result, -8)
        self.assertEqual(self.calculator.get_history(), ["-2 ^ 3 = -8"])

    def test_power_mixed_numbers(self):
        result = self.calculator.power(4, -0.5)
        self.assertEqual(result, 0.5)
        self.assertEqual(self.calculator.get_history(), ["4 ^ -0.5 = 0.5"])

    def test_power_floats(self):
        result = self.calculator.power(2.5, 2.0)
        self.assertEqual(result, 6.25)
        self.assertEqual(self.calculator.get_history(), ["2.5 ^ 2.0 = 6.25"])

    def test_get_history(self):
        self.calculator.add(1, 2)
        self.calculator.subtract(3, 1)
        history = self.calculator.get_history()
        self.assertEqual(history, ["1 + 2 = 3", "3 - 1 = 2"])

    def test_clear_history(self):
        self.calculator.add(1, 2)
        self.calculator.clear_history()
        self.assertEqual(self.calculator.get_history(), [])

    def test_multiple_operations_history(self):
        self.calculator.add(5, 5)
        self.calculator.subtract(10, 2)
        self.calculator.multiply(4, 2)
        self.calculator.divide(16, 2)
        self.calculator.power(3, 2)
        expected_history = ["5 + 5 = 10", "10 - 2 = 8", "4 * 2 = 8", "16 / 2 = 8.0", "3 ^ 2 = 9"]
        self.assertEqual(self.calculator.get_history(), expected_history)


if __name__ == '__main__':
    unittest.main()