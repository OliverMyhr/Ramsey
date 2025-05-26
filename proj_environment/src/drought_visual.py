import os
import io
import zipfile
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Laster ned og pakker ut shapefiles for US counties
def download_us_county_shapefile(folder="shapefiles"):
    url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip"
    shapefile_path = os.path.join(folder, "cb_2022_us_county_500k.shp")

    if not os.path.exists(shapefile_path):
        print("Laster ned shapefile...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        os.makedirs(folder, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(folder)
    return shapefile_path

# Statistisk kart over temperatur for gitt dato
def plot_temperature_map(date: str, csv_path: str = "../data/filtered_temperature_data.csv"):
    df = pd.read_csv(csv_path)
    df_date = df[df["date"] == date]

    if df_date.empty:
        print(f"Ingen data funnet for {date}")
        return

    shapefile_path = download_us_county_shapefile() 
    counties = gpd.read_file(shapefile_path)

    counties["fips"] = (counties["STATEFP"] + counties["COUNTYFP"]).astype(int)
    merged = counties.merge(df_date, on="fips", how="inner")

    merged.plot(
        column="T2M",
        figsize=(15, 10),
        legend=True,
        cmap="coolwarm",
        edgecolor="black",
        linewidth=0.1
    )
    plt.title(f"Temperatur per fylke - {date}", fontsize=16)
    plt.axis("off")
    plt.show()

# Statistisk kart over nedbør
def plot_precipitation_map(date: str, csv_path: str = "../data/filtered_precipitation_data.csv"):
    df = pd.read_csv(csv_path)
    df_date = df[df["date"] == date]

    if df_date.empty:
        print(f"Ingen data funnet for {date}")
        return

    shapefile_path = download_us_county_shapefile()  
    counties = gpd.read_file(shapefile_path)

    counties["fips"] = (counties["STATEFP"] + counties["COUNTYFP"]).astype(int)
    merged = counties.merge(df_date, on="fips", how="inner")

    merged.plot(
        column="PRECTOT",
        figsize=(15, 10),
        legend=True,
        cmap="Blues",  
        edgecolor="black",
        linewidth=0.1
    )
    plt.title(f"Nedbør per fylke - {date}", fontsize=16)
    plt.axis("off")
    plt.show()

# Interaktivt temperaturkart med hover og zoom
def plot_interactive_temperature_map(date: str, csv_path: str = "../data/filtered_temperature_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df_date = df[df["date"] == date]

    if df_date.empty:
        print(f"Ingen data funnet for {date}")
        return

    shapefile_path = download_us_county_shapefile()
    counties = gpd.read_file(shapefile_path)
    counties["fips"] = (counties["STATEFP"] + counties["COUNTYFP"]).astype(int)

    merged = counties.merge(df_date, on="fips", how="inner")
    merged = merged.to_crs(epsg=4326) 

    fig = px.choropleth(
        merged,
        geojson=merged.geometry.__geo_interface__,
        locations=merged.index,
        color="T2M",
        hover_name="NAME",
        hover_data={"fips": True, "T2M": True},
        color_continuous_scale="RdBu_r",
        title=f"Temperatur per fylke – {date}",
    )

    fig.update_geos(fitbounds="locations",
        visible=False,
        showcountries=True,
        showcoastlines=False,
        showland=True,)
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                dragmode=False,
                geo=dict(projection_scale=1,
                center={"lat": 37.0902, "lon": -95.7129}, ))
    fig.show()

# Plotter temperatur for en spesifikk fips kode
def plot_temperature_for_day_and_fips(dato_str, fips_kode, csv_path="../data/filtered_temperature_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])

    try:
        dag, måned = map(int, dato_str.strip().split("-"))
    except:
        print("Feil datoformat. Bruk f.eks. '15-03' for 15. mars.")
        return

    df_filtered = df[
        (df["fips"] == int(fips_kode)) &
        (df["date"].dt.day == dag) &
        (df["date"].dt.month == måned)
    ]

    if df_filtered.empty:
        print("Ingen data funnet for valgt dato og FIPS-kode.")
        return

    df_filtered = df_filtered.copy()
    df_filtered["year"] = df_filtered["date"].dt.year
    df_filtered = df_filtered.sort_values("year")

    plt.figure(figsize=(10, 6))
    plt.plot(df_filtered["year"], df_filtered["T2M"], marker="o")
    plt.title(f"Temperatur {dag:02d}.{måned:02d} for FIPS {fips_kode}")
    plt.xlabel("År")
    plt.ylabel("Temperatur")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plotter temperatur per år for en fips kode
def plot_temperature_for_fips(fips_kode, csv_path="../data/filtered_temperature_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df_filtered = df[df["fips"] == int(fips_kode)].copy()

    if df_filtered.empty:
        print(f"Ingen data funnet for FIPS-kode {fips_kode}.")
        return
    
    df_filtered["year"] = df_filtered["date"].dt.year

    yearly_avg = df_filtered.groupby("year")["T2M"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(yearly_avg["year"], yearly_avg["T2M"], marker="o", color="royalblue", linewidth=2)

    plt.title(f"Gjennomsnittstemperatur for FIPS {fips_kode} per år", fontsize=16, fontweight="bold")
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Gjennomsnittlig temperatur (T2M)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plotter nedbør per år for en fips kode
def plot_precipitation_for_fips(fips_kode, csv_path="../data/filtered_precipitation_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df_filtered = df[df["fips"] == int(fips_kode)].copy()

    if df_filtered.empty:
        print(f"Ingen data funnet for FIPS-kode {fips_kode}.")
        return
    
    df_filtered["year"] = df_filtered["date"].dt.year

    yearly_avg = df_filtered.groupby("year")["PRECTOT"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(yearly_avg["year"], yearly_avg["PRECTOT"], marker="o", color="navy", linewidth=2)

    plt.title(f"Gjennomsnittlig nedbør for FIPS {fips_kode} per år", fontsize=16, fontweight="bold")
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Gjennomsnittlig nedbør (PRECTOT)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plotter nedbør per måned for ett år
def plot_monthly_precipitation_for_year(year, csv_path="../data/filtered_precipitation_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    
    df_year = df[df["date"].dt.year == int(year)].copy()

    if df_year.empty:
        print(f"Ingen data funnet for året {year}.")
        return

    df_year["month"] = df_year["date"].dt.month
    monthly_avg = df_year.groupby("month")["PRECTOT"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg["month"], monthly_avg["PRECTOT"], marker="o", color="royalblue", linewidth=2)

    plt.title(f"Gjennomsnittlig nedbør per måned – {year}", fontsize=16, fontweight="bold")
    plt.xlabel("Måned", fontsize=12)
    plt.ylabel("Gjennomsnittlig nedbør", fontsize=12)
    plt.xticks(ticks=range(1, 13), labels=[
        "Jan", "Feb", "Mar", "Apr", "Mai", "Jun", 
        "Jul", "Aug", "Sep", "Okt", "Nov", "Des"])
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# Plotter nedbør for en måned vist per år
def plot_yearly_precipitation_for_month(month, csv_path="../data/filtered_precipitation_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    df_month = df[df["month"] == int(month)].copy()

    if df_month.empty:
        print(f"Ingen data funnet for måned {month}.")
        return

    yearly_avg = df_month.groupby("year")["PRECTOT"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(yearly_avg["year"], yearly_avg["PRECTOT"], marker="o", color="royalblue", linewidth=2)

    month_names = [
        "Januar", "Februar", "Mars", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Desember"
    ]

    plt.title(f"Gjennomsnittlig nedbør i {month_names[month-1]} per år", fontsize=16, fontweight="bold")
    plt.xlabel("År", fontsize=12)
    plt.ylabel("Gjennomsnittlig nedbør (PRECTOT)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Lager en grid med linjeplot for gjenomsnittstemperatur per måned over år
def plot_monthly_temp_facets(csv_path="../data/filtered_temperature_data.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    monthly_avg = df.groupby(["year", "month"])["T2M"].mean().reset_index()

    g = sns.FacetGrid(monthly_avg, col="year", col_wrap=4, height=3.5, aspect=1.2)
    g.map_dataframe(sns.lineplot, x="month", y="T2M", marker="o", color="royalblue")
    g.set_axis_labels("Måned", "Temperatur (°C)")
    g.set_titles("År {col_name}")
    g.set(xticks=range(1, 13))
    g.fig.subplots_adjust(top=0.92)
    g.fig.suptitle("Gjennomsnittstemperatur per måned over år", fontsize=16)

    plt.show()