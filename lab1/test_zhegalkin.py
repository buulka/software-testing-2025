import unittest
from unittest.mock import patch
from io import StringIO
import sys

sys.path.append('.')
from zhegalkin import row_xor, make_triangle, make_polynomial, draw_triangle


class TestZhegalkin(unittest.TestCase):

    def test_row_xor_basic(self):
        """Тест базового XOR преобразования строки"""
        # Arrange
        test_row = [1, 0, 1, 0]
        expected = [1, 1, 1]

        # Act
        result = row_xor(test_row)

        # Assert
        self.assertEqual(result, expected)

    def test_row_xor_single_element(self):
        """Тест граничного случая - строка с одним элементом"""
        # Arrange
        test_row = [1]
        expected = []

        # Act
        result = row_xor(test_row)

        # Assert
        self.assertEqual(result, expected)

    def test_make_triangle_2_variables(self):
        """Тест построения треугольника для 2 переменных"""
        # Arrange
        table = [
            [0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        n = 2
        expected_triangle = [
            [0, 1, 1, 0],
            [1, 0, 1],
            [1, 1],
            [0]
        ]

        # Act
        result = make_triangle(table, n)

        # Assert
        self.assertEqual(result, expected_triangle)

    def test_make_polynomial_2_variables(self):
        """Тест формирования полинома для 2 переменных"""
        # Arrange
        triangle = [
            [0, 1, 1, 0],
            [1, 0, 1],
            [1, 1],
            [0]
        ]
        n = 2
        expected_coeffs = [0, 1, 1, 0]

        # Act
        coeffs, polynomial = make_polynomial(triangle, n)

        # Assert
        self.assertEqual(coeffs, expected_coeffs)
        self.assertTrue("A" in polynomial and "B" in polynomial or
                        polynomial == "A + B" or polynomial == "B + A")


    def test_make_triangle_empty(self):
        """Тест граничного случая - пустая таблица"""
        # Arrange
        table = []
        n = 0

        # Act
        result = make_triangle(table, n)

        # Assert
        self.assertEqual(result, [])

    def test_make_triangle_single_row(self):
        """Тест с одной строкой"""
        # Arrange
        table = [[0, 1]]
        n = 1
        expected_triangle = [
            [1],
            []
        ]

        # Act
        result = make_triangle(table, n)

        # Assert
        self.assertEqual(result, expected_triangle)

    @patch('sys.stdout', new_callable=StringIO)
    def test_draw_triangle(self, mock_stdout):
        """Тест отрисовки треугольника"""
        # Arrange
        triangle = [
            [0, 1, 1, 0],
            [1, 0, 1],
            [1, 1],
            [0]
        ]

        # Act
        draw_triangle(triangle)
        output = mock_stdout.getvalue()

        # Assert
        self.assertTrue(len(output) > 0)
        self.assertIn("  ", output)


if __name__ == '__main__':
    unittest.main()
