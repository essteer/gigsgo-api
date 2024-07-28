import unittest
from fastapi.testclient import TestClient
from src.main import get_app

class TestFastAPIApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = get_app()
        cls.client = TestClient(app)

    def test_read_main(self):
        """Test main page status OK"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_static_files(self):
        """Test main CSS status OK"""
        response = self.client.get("/static/css/main.css")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    