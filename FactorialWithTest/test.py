# test_factorial.py
import unittest
from factorial import fatorial  # Importa a função do arquivo factorial.py

class TestFatorial(unittest.TestCase):

    def test_fatorial_positivo(self):
        # Testando o fatorial de números positivos
        self.assertEqual(fatorial(5), 120)
        self.assertEqual(fatorial(3), 6)
        self.assertEqual(fatorial(1), 1)

    def test_fatorial_zero(self):
        # Testando o fatorial de zero (deve ser 1)
        self.assertEqual(fatorial(0), 1)

    def test_fatorial_negativo(self):
        # Testando o comportamento com número negativo
        with self.assertRaises(ValueError):
            fatorial(-5)

    def test_fatorial_grande(self):
        # Testando um valor maior
        self.assertEqual(fatorial(10), 3628800)

if __name__ == "__main__":
    unittest.main(verbosity=2)
