import requests
import zipfile
import io
import pandas as pd
import os

url = "https://www.kaggle.com/api/v1/datasets/download/cdminix/us-drought-meteorological-data"

#Funksjon for å laste ned zip-filen fra URL
def download_zip(url):
    response = requests.get(url)
    return response

#Funksjon for å åpne zip-filen og vise innholdet
def open_zip(response):
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    print("Filer i ZIP:", zip_file.namelist())
    return zip_file

#Funksjon for å hente CSV-filen fra zip-filen
def get_csv_filename(zip_file):
    return zip_file.namelist()[2]  

#Funksjon for å lese CSV-filen fra zip-filen
def read_csv_from_zip(zip_file, csv_filename):
    with zip_file.open(csv_filename) as csv_file:
        df = pd.read_csv(csv_file)  
    return df

#Funksjon for å skrive ut noen unike FIPS-koder, som man kan velge fra
def print_unique_fips(df):
    unique_fips = df['fips'].unique()
    return f"Unike FIPS koder: {unique_fips[:20]}"

#Funksjon for å filtrere data basert på valgte FIPS koder
def filter_data(df, selected_fips):
    filtered_df = df[df['fips'].isin(selected_fips)]
    return filtered_df

#Funksjon for å lagre filtrert data til CSV-fil i mappen data
def save_filtered_data(filtered_df):
    filtered_df.to_csv('../data/filtered1_data.csv', index=False)
    print(f"Første rader i filtrert datasett: {filtered_df.head()}")

#Funksjon for å lagre temperaturdata til CSV-fil i mappen data (dette skal brukes til visualisering)
def save_temperature_data(filtered_df):
    temp_df = filtered_df[['fips', 'date', 'T2M']] #Velger nødvenige kolonner
    temp_df.to_csv('../data/filtered_temperature_data.csv', index=False)
    print(f"Første rader i filtrert datasett: {temp_df.head()}")

#Funksjon for å lagre nedbørsdata til CSV-fil i mappen data (dette skal brukes til visualisering)
def save_precipitation_data(filtered_df):
    prec_df = filtered_df[['fips', 'date', 'PRECTOT']] #Velger nødvendige kolonner
    prec_df.to_csv('../data/filtered_precipitation_data.csv', index=False)
    print(f"Første rader i filtrert datasett: {prec_df.head()}")


def new_file():
    while True:
        try:
            new = input("Ønsker du å lage en ny fil? (y/n): ")

            if new.lower() == "y":

                print("Lager ny fil...")

                #Kjører tidligere definerte funksjoner for å danne ny fil (vil erstatte eksisterende fil hvis filnavnet er likt)

                response = download_zip(url)
                zip_file = open_zip(response)
                csv_filename = get_csv_filename(zip_file)
                df = read_csv_from_zip(zip_file, csv_filename)
                print_unique_fips(df)
                selected_fips = [1001, 1003, 1005] #Eksempel på FIPS koder, kan endres
                filtered_df = filter_data(df, selected_fips)
                
                save_filtered_data(filtered_df)
                save_temperature_data(df)
                save_precipitation_data(df)

                print(f"Antall rader etter filtrering: {len(filtered_df)}") #For å få en oversikt over størrelse på fil, og hva man kan gjøre med den

                break

            elif new.lower() == "n":

                print("Ingen ny fil dannet.")

                break

            else:

                print("Invalid input, vennligst skriv 'y' eller 'n'")

        except Exception as e:
            print(f"En feilmelding oppsto: {e}")

new_file()