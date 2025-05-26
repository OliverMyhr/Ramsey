import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Plotter døgnvariasjon for air-temperature, humidity og wind
def polar_plot(filepath="../data/final_data.json"):
    try:
        # Last inn DataFrame
        df = pd.read_json(filepath)

        # Klargjør DataFrame
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])
        df["element_with_unit"] = df["elementId"]
        df["hour"] = df["referenceTime"].dt.hour

        # Grupperer stasjon, element og time
        grouped = df.groupby(["sourceId", "element_with_unit", "hour"])["avg_value"].mean().reset_index()

        # Polar-plot per stasjon og variabel
        for (element, station), subset in grouped.groupby(["element_with_unit", "sourceId"]):
            theta = 2 * np.pi * subset["hour"] / 24
            r = subset["avg_value"]

            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(theta, r, marker="o")
            ax.set_title(f"Døgnvariasjon ({element}) - {station}")
            ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
            ax.set_xticklabels([f"{h}:00" for h in range(24)])
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)

            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print(f"Filen '{filepath}' ble ikke funnet.")
    except KeyError as e:
        print(f"Mangler forventet kolonne i datasettet: {e}")
    except Exception as e:
        print(f"Noe gikk galt: {e}")

# Plotter gjennomsnittverdiene for air-temperature, humidity og wind, per måned
def plot_monthly_average(filepath="../data/final_data.json"):
    try:
        # Last inn DataFrame
        df = pd.read_json(filepath)

        # Konverter tid og klargjør kolonner
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])
        df["month"] = df["referenceTime"].dt.month
        df["element_with_unit"] = df["elementId"]

        # Lag tom månedstabell
        full_months_df = pd.DataFrame({"month": list(range(1, 13))})

        # Beregn gjennomsnitt per måned, stasjon og element
        grouped = df.groupby(["sourceId", "element_with_unit", "month"])["avg_value"].mean().reset_index()

        # Lager plott for gjennomsnitt per måned
        for (element, station), subset in grouped.groupby(["element_with_unit", "sourceId"]):
            # Fyll inn manglende måneder
            merged = pd.merge(full_months_df, subset, on="month", how="left")

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(merged["month"], merged["avg_value"], marker="o")
            ax.set_title(f"Månedsmiddel ({element}) - {station}")
            ax.set_xlabel("Måned")
            ax.set_ylabel("Gjennomsnittsverdi")
            ax.set_xticks(range(1, 13))
            ax.grid(True)

            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print(f"Filen '{filepath}' ble ikke funnet.")
    except KeyError as e:
        print(f"Mangler forventet kolonne i datasettet: {e}")
    except Exception as e:
        print(f"Noe gikk galt: {e}")" 

# Plotter ukentlig døgnmønster for air-temperature, humidity og wind
def heatmap_weekday_hour(filepath="../data/final_data.json"):
    try:
        df = pd.read_json(filepath)
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])
        df["weekday"] = df["referenceTime"].dt.dayofweek 
        df["hour"] = df["referenceTime"].dt.hour
        df["element_with_unit"] = df["elementId"]

        weekday_labels = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]

        # Plott over ukentlig døgnmønster
        for (element, station), subset in df.groupby(["element_with_unit", "sourceId"]):
            pivot = subset.pivot_table(index="weekday", columns="hour", values="avg_value", aggfunc="mean")

            fig, ax = plt.subplots(figsize=(12, 5))
            sns.heatmap(pivot, cmap="coolwarm", ax=ax, cbar_kws={"label": "Verdi"}, linewidths=0.5, linecolor="gray")
            ax.set_title(f"Ukentlig døgnmønster ({element}) – {station}")
            ax.set_xlabel("Time på døgnet")
            ax.set_ylabel("Ukedag")
            ax.set_yticks(np.arange(7) + 0.5)
            ax.set_yticklabels(weekday_labels, rotation=0)

            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print(f"Filen '{filepath}' ble ikke funnet.")
    except KeyError as e:
        print(f"Mangler forventet kolonne i datasettet: {e}")
    except Exception as e:
        print(f"Noe gikk galt: {e}")
