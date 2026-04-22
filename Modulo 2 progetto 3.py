# ============================================================
# Progetto #3 — Creare una Dashboard Avanzata di Visualizzazione
# ============================================================
#
# Traccia:
# Realizzare una dashboard interattiva per analizzare i dati di vendita
# e redditività di un negozio online, usando Python
# (Pandas + Plotly Dash / Streamlit / Matplotlib / Seaborn).
#
# ---
# Struttura del dataset:
# - Order Date    -> Data dell'ordine
# - Ship Date     -> Data di spedizione
# - Category      -> Categoria prodotto (es. Furniture, Office Supplies, Technology)
# - Sub-Category  -> Sottocategoria prodotto
# - Sales         -> Vendite (€)
# - Profit        -> Utile (€)
# - Region        -> Area geografica
# - State         -> Stato/Regione
# - Quantity      -> Quantità venduta
#
# ---
# Consegna
#
# Parte 1 – Pulizia dati
# 1. Convertire le colonne data (Order Date, Ship Date) in formato datetime.
# 2. Controllare valori nulli e duplicati.
# 3. Creare una nuova colonna Year dall'Order Date.
#
# Parte 2 – Analisi Esplorativa (EDA)
# 4. Totale vendite e profitti per anno.
# 5. Top 5 sottocategorie più vendute.
# 6. Mappa interattiva delle vendite.
# ============================================================

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

CSV_PATH = "superstore.csv"

# ============================================================
# GENERAZIONE DATASET SINTETICO (solo al primo run)
# ============================================================
# Non avendo il file originale, creiamo un dataset fittizio ma realistico
# che rispetta la struttura richiesta dalla traccia.
if not os.path.exists(CSV_PATH):
    rng = np.random.default_rng(42)
    n = 5000

    categories_subs = {
        "Furniture": ["Bookcases", "Chairs", "Tables", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Art",
                            "Appliances", "Envelopes", "Labels", "Supplies"],
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
    }
    cat_sub_pairs = [(c, s) for c, subs in categories_subs.items() for s in subs]
    idx = rng.integers(0, len(cat_sub_pairs), n)
    categories = [cat_sub_pairs[i][0] for i in idx]
    sub_cats = [cat_sub_pairs[i][1] for i in idx]

    states_regions = {
        "California": "West", "Oregon": "West", "Washington": "West",
        "Nevada": "West", "Arizona": "West",
        "New York": "East", "Pennsylvania": "East", "Massachusetts": "East",
        "Virginia": "East", "Florida": "East",
        "Texas": "Central", "Illinois": "Central", "Ohio": "Central",
        "Michigan": "Central", "Missouri": "Central",
        "Georgia": "South", "North Carolina": "South", "Tennessee": "South",
        "Louisiana": "South", "Alabama": "South",
    }
    state_list = list(states_regions.keys())
    state_weights = rng.dirichlet(np.ones(len(state_list)) * 0.7)
    state_choices = rng.choice(state_list, n, p=state_weights)
    regions = [states_regions[s] for s in state_choices]

    start = datetime(2020, 1, 1)
    days_span = (datetime(2023, 12, 31) - start).days
    order_dates = [start + timedelta(days=int(d)) for d in rng.integers(0, days_span, n)]
    ship_dates = [od + timedelta(days=int(s)) for od, s in zip(order_dates, rng.integers(1, 8, n))]

    quantities = rng.integers(1, 15, n)
    unit_prices = rng.uniform(5, 500, n)
    sales = (quantities * unit_prices).round(2)
    margins = rng.normal(0.15, 0.25, n)  # alcuni margini negativi (perdite realistiche)
    profits = (sales * margins).round(2)

    df_gen = pd.DataFrame({
        "Order Date": order_dates,
        "Ship Date": ship_dates,
        "Category": categories,
        "Sub-Category": sub_cats,
        "Sales": sales,
        "Profit": profits,
        "Region": regions,
        "State": state_choices,
        "Quantity": quantities,
    })
    df_gen.to_csv(CSV_PATH, index=False)
    print(f"[setup] Dataset sintetico creato: {CSV_PATH} ({n} righe)\n")

# ---
# Caricamento dati
df = pd.read_csv(CSV_PATH)

# ============================================================
# PARTE 1 — PULIZIA DATI
# ============================================================

# 1. Date in formato datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=False)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=False)

# 2. Valori nulli e duplicati
print("Valori nulli per colonna:")
print(df.isnull().sum())
print(f"\nRighe duplicate: {df.duplicated().sum()}")
df = df.drop_duplicates()

# 3. Colonna Year
df["Year"] = df["Order Date"].dt.year

# ============================================================
# PARTE 2 — ANALISI ESPLORATIVA (EDA)
# ============================================================

sns.set_theme(style="whitegrid")

# 4. Vendite e profitti per anno
yearly = df.groupby("Year")[["Sales", "Profit"]].sum().reset_index()
print("\nTotali per anno:")
print(yearly)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.barplot(data=yearly, x="Year", y="Sales", hue="Year",
            palette="Blues_d", legend=False, ax=axes[0])
axes[0].set_title("Vendite totali per anno")
axes[0].set_ylabel("Vendite (€)")

sns.barplot(data=yearly, x="Year", y="Profit", hue="Year",
            palette="Greens_d", legend=False, ax=axes[1])
axes[1].set_title("Profitti totali per anno")
axes[1].set_ylabel("Profit (€)")
plt.tight_layout()
plt.show()

# 5. Top 5 sottocategorie più vendute (per Sales)
top5 = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)
print("\nTop 5 sottocategorie:")
print(top5)

plt.figure(figsize=(9, 5))
sns.barplot(data=top5, x="Sales", y="Sub-Category", hue="Sub-Category",
            palette="viridis", legend=False)
plt.title("Top 5 sottocategorie più vendute")
plt.xlabel("Vendite totali (€)")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 6. Mappa interattiva delle vendite per stato (USA)
state_sales = df.groupby("State")["Sales"].sum().reset_index()

# Mappa nome stato -> codice USPS (necessario per locationmode="USA-states")
us_state_codes = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}
state_sales["Code"] = state_sales["State"].map(us_state_codes)

fig_map = px.choropleth(
    state_sales,
    locations="Code",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    color_continuous_scale="Viridis",
    hover_name="State",
    hover_data={"Sales": ":,.0f", "Code": False},
    title="Vendite totali per Stato (USA)",
)
fig_map.show()
