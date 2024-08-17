import json
import os
import unittest
from pathlib import Path
from src.crud import CRUD


TESTS_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR: Path = TESTS_DIR / "test_data"
TEST_DATA_PATH: Path = TEST_DATA_DIR / "test_data.json"
TEST_DB_PATH: Path = TEST_DATA_DIR / "_test_db.json"
test_data = [
    {"_id": "1", "name": "Event 1", "date": "2024-08-15"},
    {"_id": "2", "name": "Event 2", "date": "2024-08-16"},
]


class TestCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup test database and data"""
        TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.crud = CRUD(db_path=str(TEST_DB_PATH))
        
        with open(TEST_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        
        cls.crud.init_db(init_data_path=TEST_DATA_PATH)

    @classmethod
    def tearDownClass(cls):
        """Cleanup test database and data"""
        if TEST_DB_PATH.exists():
            os.remove(TEST_DB_PATH)
        if TEST_DATA_PATH.exists():
            os.remove(TEST_DATA_PATH)
        if TEST_DATA_DIR.exists():
            os.rmdir(TEST_DATA_DIR)
            
    def test_read_all(self):
        """Test reading all items"""
        items = self.crud.read_all()
        self.assertEqual(len(items), len(test_data))

    def test_create_one(self):
        """Test adding a new item"""
        new_item = {"name": "Event 3", "date": "2024-08-17"}
        self.crud.create_one(new_item)
        items = self.crud.read_all()
        self.assertEqual(len(items), 3)
        self.assertTrue(any(item["name"] == "Event 3" for item in items))

    def test_find(self):
        """Test finding an item by key"""
        result = self.crud.find("name", "Event 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Event 1")

    def test_update_one(self):
        """Test updating an existing item"""
        updated_fields = {"name": "Updated Event 1"}
        self.crud.update_one("1", updated_fields)
        item = self.crud.find("_id", "1")
        self.assertEqual(len(item), 1)
        self.assertEqual(item[0]["name"], "Updated Event 1")

    def test_delete_one(self):
        """Test deleting an item"""
        self.crud.delete_one("2")
        items = self.crud.read_all()
        self.assertEqual(len(items), 2)

    def test_search(self):
        """Test searching items"""
        result = self.crud.search("name", "Event")
        self.assertGreater(len(result), 0)
        self.assertTrue(all("Event"in item["name"] for item in result))


if __name__ == "__main__":
    unittest.main()
