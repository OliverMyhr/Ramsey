import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from frost_data_collection import remove_outliers


def prepare_data():
    df = remove_outliers()
    df = df[df["elementId"] == "air_temperature"]
    df = df.sort_values("referenceTime")
    df["time_numeric"] = (df["referenceTime"] - df["referenceTime"].min()).dt.total_seconds()

    return df


def train_model(df):
    x = df[["time_numeric"]]
    y = df["avg_value"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Modellen er trent.\nMSE: {mse:.2f}, R²: {r2:.2f}")

    return model, x_test, y_test, y_pred


def create_visualizations(df, model, x_test, y_test, y_pred):
    sns.set(style="whitegrid")
    fig, axs = plt.subplots(3, 1, figsize=(14, 20))

    sns.lineplot(data=df, x="referenceTime", y="avg_value", ax=axs[0], color="royalblue")
    axs[0].set_title("Temperatur over tid (linjediagram)")
    axs[0].set_ylabel("Temperatur (°C)")
    axs[0].set_xlabel("Tid")

    axs[1].scatter(x_test, y_test, color="black", label="Reelle verdier", alpha=0.6)
    axs[1].plot(x_test, y_pred, color="red", linewidth=2, label="Modellens prediksjon")
    axs[1].set_title("Prediksjon vs Reelle temperaturverdier (scatterplot + linje)")
    axs[1].set_ylabel("Temperatur (°C)")
    axs[1].set_xlabel("Tid (sekunder siden start)")
    axs[1].legend()

    df_monthly = df.copy()
    df_monthly["month"] = df_monthly["referenceTime"].dt.month
    avg_per_month = df_monthly.groupby("month")["avg_value"].mean().reset_index()

    sns.barplot(data=avg_per_month, x="month", y="avg_value", palette="coolwarm", ax=axs[2])
    axs[2].set_title("Gjennomsnittstemperatur per måned (søylediagram)")
    axs[2].set_ylabel("Temperatur (°C)")
    axs[2].set_xlabel("Måned")

    plt.show()


def visualize_missing_data(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    df_missing = df.copy()
    df_missing.loc[::10, "avg_value"] = np.nan
    plt.plot(df_missing["referenceTime"], df_missing["avg_value"], label="Med manglende verdier", color="gray", linestyle="--")
    plt.plot(df["referenceTime"], df["avg_value"], label="Originale verdier", color="green", alpha=0.7)
    plt.title("Effekt av manglende verdier på temperaturtrend")
    plt.ylabel("Temperatur (°C)")
    plt.xlabel("Tid")
    plt.legend()
    plt.tight_layout()

    plt.show()