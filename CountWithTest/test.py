import unittest
from count import contador  

class TestStringMethods(unittest.TestCase):
    def test_01_contador_retorna_dic(self):
        d = contador('o doce mais doce')
        self.assertEqual(type(d), type({'dicionario': 'exemplo'}), "Passou no Teste")

    def test_02_contador(self):
        d = contador("o doce mais doce")
        self.assertEqual(d, {"o": 1, "mais": 1, "doce": 2})

        d2 = contador('esse exercício é um exercício fácil ou difícil')
        self.assertEqual(d2, {
            'é': 1, 'difícil': 1, 'esse': 1, 'ou': 1, 'um': 1, 'fácil': 1, 'exercício': 2
        })

        d3 = contador('o doce perguntou ao doce qual é o doce mais doce ' +
                      'e o doce respondeu ao doce que o doce mais doce é ' +
                      'o doce de batata doce')
        self.assertEqual(d3['doce'], 10)
        self.assertTrue('gato' not in d3)
        self.assertTrue('respondeu' in d3)

if __name__ == "__main__":
    unittest.main(verbosity=2)