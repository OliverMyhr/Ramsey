import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
from requests.exceptions import RequestException


proj_root = os.path.abspath("..") 
sys.path.insert(0, os.path.join(proj_root, "proj_environment", "src"))

from frost_data_collection import (
    json_file, test_params, to_df, clean, analyze, final_data
)

class TestFrostModule(unittest.TestCase):

    def setUp(self):
        self.valid_response = {
            "data": [
                {
                    "sourceId": "SN18700:0",
                    "referenceTime": "2023-01-01T00:00:00Z",
                    "observations": [
                        {"elementId": "air_temperature", "value": 1.0, "unit": "degC"}
                    ]
                }
            ]
        }

    @patch("requests.get")
    def test_json_file_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.valid_response
        mock_get.return_value = mock_response

        result = json_file(test_params)
        self.assertIsInstance(result, dict)
        self.assertIn("data", result)

    @patch("requests.get", side_effect=RequestException("API-feil"))
    def test_json_file_failure(self, mock_get):
        result = json_file(test_params)
        self.assertIn("Data kunne ikke hentes", result)


    @patch("frost_data_collection.json_file")
    def test_to_df_valid(self, mock_json_file):
        mock_json_file.return_value = self.valid_response
        df = to_df()
        self.assertFalse(df.empty)
        self.assertIn("elementId", df.columns)

    def test_clean_removes_na(self):
        df = pd.DataFrame({"value": [1.0, None, 2.0]})
        cleaned = clean(df)
        self.assertEqual(len(cleaned), 2)
        self.assertFalse(cleaned.isnull().values.any())

    def test_analyze_returns_avg_value(self):
        df = pd.DataFrame({
            "referenceTime": ["2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z"],
            "sourceId": ["SN18700:0", "SN18700:0"],
            "elementId": ["air_temperature", "air_temperature"],
            "value": [1.0, 2.0],
            "unit": ["degC", "degC"]
        })
        result = analyze(df)
        self.assertIn("avg_value", result.columns)

    @patch("frost_data_collection.to_df")
    def test_final_data_valid(self, mock_to_df):
        df = pd.DataFrame({
            "referenceTime": ["2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z"],
            "sourceId": ["SN18700:0", "SN18700:0"],
            "elementId": ["air_temperature", "air_temperature"],
            "value": [1.0, 2.0],
            "unit": ["degC", "degC"]
        })
        mock_to_df.return_value = df
        result = final_data()
        self.assertFalse(result.empty)
        self.assertIn("avg_value", result.columns)

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestFrostModule))

