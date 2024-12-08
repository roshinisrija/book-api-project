import unittest
from app import app

class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)

    def test_add_book(self):
        response = self.app.post('/books', json={
            "title": "Test Book",
            "author": "Test Author",
            "year": 2024
        }, headers={"Authorization": "Bearer secure-token-1234"})
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
