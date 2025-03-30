import unittest
import sys
import os
import io
import zipfile
import pandas as pd
from unittest.mock import patch, MagicMock

proj_root = os.path.abspath("..")  
sys.path.insert(0, os.path.join(proj_root, "src"))

from droughtEKTE import (
    download_zip, open_zip, get_csv_filename, read_csv_from_zip, 
    print_unique_fips, filter_data, save_filtered_data
)

class TestDrought(unittest.TestCase):
    
    def setUp(self):
        self.mock_zip_content = b"Dummy zip data"
        self.mock_csv_content = "fips,value\n1001,10\n1003,20\n1005,30"
        
        self.mock_response = MagicMock()
        self.mock_response.content = self.mock_zip_content
        
        self.mock_zip_file = MagicMock()
        self.mock_zip_file.namelist.return_value = ["file1.txt", "file2.csv", "file3.csv"]
        
    @patch("requests.get")
    def test_download_zip(self, mock_get):
        mock_get.return_value = self.mock_response
        response = download_zip("https://example.com/fake.zip")
        self.assertEqual(response, self.mock_response)
    
    @patch("zipfile.ZipFile")
    def test_open_zip(self, mock_zip):
        mock_zip.return_value = self.mock_zip_file
        zip_file = open_zip(self.mock_response)
        self.assertEqual(zip_file.namelist(), ["file1.txt", "file2.csv", "file3.csv"])
    
    def test_get_csv_filename(self):
        filename = get_csv_filename(self.mock_zip_file)
        self.assertEqual(filename, "file3.csv")
    
    @patch("pandas.read_csv")
    def test_read_csv_from_zip(self, mock_read_csv):
        mock_df = pd.DataFrame({"fips": [1001, 1003, 1005], "value": [10, 20, 30]})
        mock_read_csv.return_value = mock_df
        
        df = read_csv_from_zip(self.mock_zip_file, "file3.csv")
        self.assertEqual(len(df), 3)
        self.assertTrue("fips" in df.columns)
    
    def test_print_unique_fips(self):
        df = pd.DataFrame({"fips": [1001, 1003, 1005, 1001, 1003]})
        output = print_unique_fips(df)
        self.assertIn("Unique fips-codes", output)
    
    def test_filter_data(self):
        df = pd.DataFrame({"fips": [1001, 1003, 1005, 1010], "value": [10, 20, 30, 40]})
        selected_fips = [1001, 1003]
        filtered_df = filter_data(df, selected_fips)
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(fips in selected_fips for fips in filtered_df["fips"].values))
    
    @patch("pandas.DataFrame.to_csv")
    def test_save_filtered_data(self, mock_to_csv):
        df = pd.DataFrame({"fips": [1001, 1003], "value": [10, 20]})
        save_filtered_data(df)
        mock_to_csv.assert_called_once()
        args, kwargs = mock_to_csv.call_args
        self.assertEqual(args[0], '../data/filtered1_data.csv')

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestDrought))
