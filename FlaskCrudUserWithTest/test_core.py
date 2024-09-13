import unittest
from app import meuApp

class TestGetUser(unittest.TestCase):
    def setUp(self):
        app = meuApp.test_client()
        self.response = app.get('/users')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_get_existing_user(self):
        app = meuApp.test_client()
        r = app.get('/users/1')
        data = r.json
        self.assertEqual(dict, type(data))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['nome'], 'caio')
        self.assertEqual(data['email'], 'caio@email')

if __name__ == '__main__':
    unittest.main()
