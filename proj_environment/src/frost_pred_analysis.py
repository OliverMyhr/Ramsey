# Refleksjonsdelen av oppgaven:

# Det har blitt valgt bruk av barplot (stolpediagram), linjeplot (stiplet og ikke stiplet) i tillegg til punktplot (scatterplot)
# Det kommer frem i visualiseringen at stolpediagramet fungerer dårligst, det blir mer utydelig og passer dårligere til regresjon.
# Ikke stiplet linje i samsvar med punktplot fungerer godt, hvert datapunkt er tydelig i form av punkter. 
# Minste kvadraters metode sørger for at linjen ligger nærmest mulig hvert punkt og grafen videre baserer seg på dette.
# Med linjen og punktene kommer det derfor tydelig frem en trend som linjen følger basert på tidligere data.
# Det aller beste valget er trolig ikke stiplet linjeplot i samsvar med stiplet linjeplot.
# Den stiplede linjen gir nemlig en bedre indikasjon på hvordan trenden egentlig skulle vært i forhold til regresjonsmodellen.
# Imens linjens viser forutsetningen som ikke er helt nøyaktig.
# Regresjonsmodellen er en lineær modell på formen p_1(x)=ax+b. En periodisk modell ville kanskje vært mer nøyaktig, men vanskeligere å få til.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import frost_data_analysis as fda


def fit_linear_model(x, y): # Bruker minste kvadraters metode fra matte 3 til å finne a og b, s.a y = ax + b passer best til datapunktene.
    valid = [not np.isnan(val) for val in y] 

    a_i1 = x[valid] # Første kolonne i A
    b_vector = y[valid] # b_1, b_2 osv.

    if len(b_vector) < 2:
        raise ValueError("For få punkter")

    A = np.transpose(np.array([a_i1, np.ones(len(a_i1))])) # b = b_1 for x = 0, a + b = b_2 for x = 1 osv.
    A_T = np.transpose(A)

    A_T_A = np.matmul(A_T, A)
    A_T_b = np.matmul(A_T, b_vector)

    x_hat = np.linalg.solve(A_T_A, A_T_b) # Løser A_T * A * x_hat = A_T * b_vector for x_hat som er vektoren (a, b)
    a = x_hat[0]
    b = x_hat[1]

    return a, b


def visualize_reg(): # Visualiserer data og forutsetning ved hjelp av regresjonsmodellen, visualiserer også ugyldig data.
    df = fda.remove_outliers()
    elements = {"air_temperature": "Temperatur", "relative_humidity": "Luftfuktighet", "wind_speed": "Vindhastighet"} # Kartlegger eller mapper label

    # Henter kun ut data per måned for færre punkter og mer ryddighet i plottene. Groupby var nyttig her
    for element_id, label in elements.items(): # Løper gjennom data for å definere input variabler x og y i tillegg til ugyldig data
        data = df[df["elementId"] == element_id].copy()
        data["referenceTime"] = pd.to_datetime(data["referenceTime"], errors = "coerce")
        data = data.dropna(subset = ["referenceTime"])
        data["month"] = data["referenceTime"].dt.to_period("M")

        monthly_avg = data.groupby("month")["avg_value"].mean()
        y = monthly_avg.values
        x = np.arange(len(y))
        missing = np.isnan(y)
        valid = np.logical_not(missing) 

        try:
            a, b = fit_linear_model(x, y)

        except Exception as e:
            print(f"Feil oppsto for {label}: {e}")

            continue

        predicted = a * x + b 
        unit_series = data["unit"].dropna()

        if not unit_series.empty:
            unit = unit_series.iloc[0]

        else: 
            unit = ""

        # Plotter resulatet (punktplott(scatterplot) og linjeplot med regresjonsmodellen)
        plt.figure(figsize = (10, 5))
        sns.scatterplot(x = x, y = y, hue = missing, palette = {False : "blue", True : "red"}) # Gyldig er blå punkter, ikke gyldig data er røde punkter
        plt.plot(x[valid], predicted[valid], color = "green", label = f"y = {a :.2f}x + {b :.2f}")
        plt.title(f"{label} per måned (manglende data markert)")
        plt.xlabel("Månedsindeks")
        plt.ylabel(f"{label} [{unit}]")
        plt.grid(True)
        plt.legend()
        plt.show()


def temperature_plot(): # Linje og stiplet linje plot for å vise regresjonsmodellen i forhold til faktisk data. 
    df = fda.remove_outliers()
    temp_data = df[df["elementId"] == "air_temperature"].copy()
    temp_data["referenceTime"] = pd.to_datetime(temp_data["referenceTime"], errors = "coerce")
    temp_data = temp_data.dropna(subset = ["referenceTime"])
    temp_data["month"] = temp_data["referenceTime"].dt.to_period("M")
    monthly_avg = temp_data.groupby("month")["avg_value"].mean()

    y = monthly_avg.values
    x = np.arange(len(y))
    unit_series = temp_data["unit"].dropna()

    if not unit_series.empty:
            unit = unit_series.iloc[0]

    else: 
        unit = ""

    try:
        a, b = fit_linear_model(x, y)

    except Exception as e:
        print(f"feil oppsto for temperatur. : {e}")
        a = b = None

    plt.figure(figsize = (12, 6))
    sns.lineplot(x = monthly_avg.index.astype(str), y = y, marker = "o", color = "blue", label = "Månedlig gjennomsnitt")

    if a is not None and b is not None:
        predicted = a * x + b
        plt.plot(monthly_avg.index.astype(str), predicted, color = "green", linestyle = "--", label = f"y = {a :.2f} x + {b :.2f}")

    plt.title("Månedlig gjennomsnittstemperatur")
    plt.xlabel("Måned")
    plt.ylabel(f"Temperatur [{unit}]")
    plt.xticks(rotation = 45)
    plt.grid(True)
    plt.legend()
    plt.show()


def humidity_plot(): # Seaborn bar plot denne gangen i tillegg til stiplet linjeplot, nesten samme funksjon som den over, men bare for luftfuktighet.
    df = fda.remove_outliers()
    hum_data = df[df["elementId"] == "relative_humidity"].copy()
    hum_data["referenceTime"] = pd.to_datetime(hum_data["referenceTime"], errors = "coerce")
    hum_data = hum_data.dropna(subset=["referenceTime"])
    hum_data["month"] = hum_data["referenceTime"].dt.to_period("M")
    monthly_avg = hum_data.groupby("month")["avg_value"].mean()

    y = monthly_avg.values
    x = np.arange(len(y))
    unit_series = hum_data["unit"].dropna()
    unit = unit_series.iloc[0] if not unit_series.empty else ""

    try:
        a, b = fit_linear_model(x, y)

    except Exception as e:
        print(f"Feil oppsto for luftfuktighet: {e}")
        a = b = None

    plt.figure(figsize = (12, 6))
    sns.barplot(x = monthly_avg.index.astype(str), y = y, color = "skyblue", label = "Månedlig gjennomsnitt") # Stolpediagram lignende

    if a is not None and b is not None:
        predicted = a * x + b
        plt.plot(monthly_avg.index.astype(str), predicted, color = "green", linestyle = "--", label = f"y = {a :.2f} x + {b :.2f}")

    plt.title("Månedlig gjennomsnittlig luftfuktighet")
    plt.xlabel("Måned")
    plt.ylabel(f"Luftfuktighet [{unit}]")
    plt.xticks(rotation = 45)
    plt.grid(axis = "y")
    plt.legend()
    plt.show()