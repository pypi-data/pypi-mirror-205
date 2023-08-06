# test_example.py
import unittest
from tresto import TrestoTestCase
from arithmetic import add, subtract, multiply, divide

class TestArithmetic(TrestoTestCase):
    auto_create_board = True
    auto_create_lists = True

    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

if __name__ == '__main__':
    unittest.main()
