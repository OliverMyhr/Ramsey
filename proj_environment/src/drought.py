import requests
import zipfile
import io
import pandas as pd


url = "https://www.kaggle.com/api/v1/datasets/download/cdminix/us-drought-meteorological-data"

response = requests.get(url)
        
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        
print("Filer i ZIP:", zip_file.namelist())

csv_filename = zip_file.namelist()[0]  
with zip_file.open(csv_filename) as csv_file:
    df = pd.read_csv(csv_file)
        
print("CSV-fil lastet inn i pandas!")
print(df.head()) 

   