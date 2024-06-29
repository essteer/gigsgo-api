import os
import unittest
from dotenv import load_dotenv
from src.app import data_pipeline
from tests.assets.ex01 import HTML_1
from tests.assets.ex02 import HTML_2
from tests.assets.ex03 import HTML_3
from tests.assets.ex04 import HTML_4


load_dotenv()

TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
TEST_CASES = [HTML_1, HTML_2, HTML_3, HTML_4]


class TestDataPipeline(unittest.TestCase):
    def test_all_matches_persist(self):
        """Test all matches retained after formatting"""
        num_matches = {HTML_1: 93, HTML_2: 113, HTML_3: 89, HTML_4: 115}
        for test_case in TEST_CASES:
            self.assertEqual(
                sum(1 for _ in data_pipeline(test_case, False)), num_matches[test_case]
            )
        # NOTE: this test relies on external source, check source if not found
        self.assertEqual(sum(1 for _ in data_pipeline(os.environ["EXAMPLE"])), 84)

    def test_matches_are_dicts(self):
        """Test all matches in dict format"""
        for test_case in TEST_CASES:
            matches = data_pipeline(test_case, False)
            for match in matches:
                self.assertIsInstance(match, dict)
        # NOTE: this test relies on external source, check source if not found
        matches = data_pipeline(os.environ["EXAMPLE"])
        for match in matches:
            self.assertIsInstance(match, dict)

    def test_expected_fields_present(self):
        """Test expected fields present"""
        for test_case in TEST_CASES:
            matches = data_pipeline(test_case, False)
            for match in matches:
                self.assertIn("weekday", match)
                self.assertIn("month", match)
                self.assertIn("date", match)
                self.assertIn("desc", match)
                self.assertIn("venue", match)
                self.assertIn("open", match)
                self.assertIn("close", match)
                self.assertIn("bands", match)
                self.assertIn("tickets", match)
        # NOTE: this test relies on external source, check source if not found
        matches = data_pipeline(os.environ["EXAMPLE"])
        for match in matches:
            self.assertIn("weekday", match)
            self.assertIn("month", match)
            self.assertIn("date", match)
            self.assertIn("desc", match)
            self.assertIn("venue", match)
            self.assertIn("open", match)
            self.assertIn("close", match)
            self.assertIn("bands", match)
            self.assertIn("tickets", match)


if __name__ == "__main__":
    unittest.main()