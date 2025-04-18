import requests
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as pdsql
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

from frost import final_data


def pivot_data():
    df = final_data()
    pivot = df.pivot_table(values = "avg_value", index = "referenceTime", columns = "elementId")

    return pivot


def statistics():
    df = final_data()

    if df.empty:
        return "DataFrame er tom."
    
    stats = df.groupby(["sourceId", "elementId", "unit"])["avg_value"].agg(["mean", "median", "std", "min", "max", "count"])

    return stats


def relation_analysis():
    pivot = pivot_data()

    if len(pivot.columns) < 2:
        return "Ikke nok elementer for å beregne sammenhenger."

    relation = pivot.corr()

    return f"Skala mellom -1 og 1, der 1 betyr sterk sammenheng, tall nærmere 0 betyr svak sammenheng.\n\n{relation}"


def relation_analysis_plots():
    pivot = pivot_data()    
    relation = pivot.corr()

    fig, axs = plt.subplots(1, 2, figsize = (15, 5))

    try:
        sns.heatmap(relation, annot = True, cmap = "coolwarm", fmt = ".2f", square = True, ax = axs[0])
        axs[0].set_title("Sammenheng mellom elementer")
    
    except Exception as e:
            print("Feil under plotting", e)
            fig.delaxes(axs[0])

    if "air_temperature" in pivot.columns and "relative_humidity" in pivot.columns:
        sns.scatterplot(x = pivot["air_temperature"], y = pivot["relative_humidity"], ax = axs[1])
        axs[1].set_xlabel("Temperatur [°C]")
        axs[1].set_ylabel("Luftfuktighet [%]")
        axs[1].set_title("Temperatur vs Luftfuktighet")
        axs[1].grid(True)

    else:
        fig.delaxes(axs[1])
        print("Manglende data")

    plt.show()


def find_outliers():
    df = final_data()

    k1 = df["avg_value"].quantile(0.25)
    k3 = df["avg_value"].quantile(0.75)

    ikv = k3 - k1
    lower = k1 - 1.5 * ikv
    upper = k3 + 1.5 * ikv

    outliers = df[(df["avg_value"] < lower) | (df["avg_value"] > upper)]

    print(f"Antall avvik: {len(outliers)}\n")

    return outliers


def remove_outliers():
    df = final_data()

    k1 = df["avg_value"].quantile(0.25)
    k3 = df["avg_value"].quantile(0.75)

    ikv = k3 - k1
    lower = k1 - 1.5 * ikv
    upper = k3 + 1.5 * ikv

    removed = df[(df["avg_value"] >= lower) & (df["avg_value"] <= upper)]

    return removed


def final_df_plots():
    df = remove_outliers()

    fig, axs = plt.subplots(2, 1, figsize = (10, 10))

    try:
        df["time_index"] = np.arange(len(df))

        sns.lineplot(data = df, x = "time_index", y = "avg_value", hue = "sourceId", style = "elementId", ax = axs[0])
        axs[0].set_title("Gjennomsnittsverdier over tid")
        axs[0].set_xlabel("Tid")
        axs[0].set_ylabel("Verdi")
        axs[0].grid(True)
        axs[0].legend()
      
        df["referenceTime"] = pd.to_datetime(df["referenceTime"])

        first_date = df["referenceTime"].iloc[0]
        last_date = df["referenceTime"].iloc[-1]

        axs[0].set_xticks([df["time_index"].iloc[0], df["time_index"].iloc[-1]])
        axs[0].set_xticklabels([first_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d")])

    except Exception as e:
        print("Feil oppsto", e)
        fig.delaxes(axs[0])
    
    try:
        df["element_with_unit"] = df["elementId"] + " [" + df["unit"].astype(str) + "]"

        sns.boxplot(data = df, x = "sourceId", y = "avg_value", hue = "element_with_unit", ax = axs[1])
        axs[1].set_title("Boksplot per stasjon")
        axs[1].set_xlabel("Stasjon")
        axs[1].set_ylabel("Verdi")
        axs[1].grid(True)
        axs[1].legend()
    
    except Exception as e:
        print("Feil oppsto", e)
        fig.delaxes(axs[1])

    plt.subplots_adjust(hspace = 0.4)

    plt.show()