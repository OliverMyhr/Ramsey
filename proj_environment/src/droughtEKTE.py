import requests
import zipfile
import io
import pandas as pd
import os

url = "https://www.kaggle.com/api/v1/datasets/download/cdminix/us-drought-meteorological-data"

def download_zip(url):
    response = requests.get(url)
    return response

def open_zip(response):
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    print("Files in ZIP:", zip_file.namelist())
    return zip_file

def get_csv_filename(zip_file):
    return zip_file.namelist()[2]  

def read_csv_from_zip(zip_file, csv_filename):
    with zip_file.open(csv_filename) as csv_file:
        df = pd.read_csv(csv_file)  
    return df

def print_unique_fips(df):
    unique_fips = df['fips'].unique()
    return f"Unique fips-codes: {unique_fips[:20]}"

def filter_data(df, selected_fips):
    filtered_df = df[df['fips'].isin(selected_fips)]
    return filtered_df

def save_filtered_data(filtered_df):
    filtered_df.to_csv('../data/filtered1_data.csv', index=False)
    print(f"First rows in the filtered dataset: {filtered_df.head()}")

def new_file():
    while True:
        try:
            new = input("Do you wish to create a new file? (y/n): ")

            if new.lower() == "y":

                print("Creating new file")
                response = download_zip(url)
                zip_file = open_zip(response)
                csv_filename = get_csv_filename(zip_file)
                df = read_csv_from_zip(zip_file, csv_filename)
                print_unique_fips(df)
                selected_fips = [1001, 1003, 1005]
                filtered_df = filter_data(df, selected_fips)
                save_filtered_data(filtered_df)

                print(f"Amount of rows after filtering: {len(filtered_df)}")

                break

            elif new.lower() == "n":

                print("No new file created")

                break

            else:

                print("Invalid input, please enter 'y' or 'n'")

        except Exception as e:
            print(f"An error occured: {e}")

new_file()