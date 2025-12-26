# ------------------------------------------------------------
# Progetto #1 — Previsioni vendite
#
# Traccia:
# L’obiettivo è lavorare su un dataset di vendite storiche per:
# - comprendere la struttura dei dati
# - pulirli e trasformarli
# - produrre semplici previsioni usando Pandas e metodi base
#
# Dataset (esempio di struttura):
#   Data       — data della vendita
#   Prodotto   — nome o codice prodotto
#   Vendite    — quantità venduta quel giorno
#   Prezzo     — prezzo unitario (opzionale)
#
# Note:
# I dati possono contenere valori mancanti, duplicati o inconsistenze.
#
# ------------------------------------------------------------
# fonte dataset: https://www.kaggle.com/datasets/pranalibose/amazon-seller-order-status-prediction
# il dataset originale è stato modificato selezionando le colonne richieste e inserendo degli errori per lo svolgimento dell'esercizio

import pandas as pd
import matplotlib.pyplot as plt


# Parte 1 — Caricamento ed esplorazione dati
# 1. Leggere il dataset con Pandas.
# 2. Visualizzare:
#       - prime righe (head)
#       - struttura (.info())
#       - statistiche descrittive (.describe())
df = pd.read_csv("orders_data_dirty.csv")
print(df.info() , "\n")
print(df.head() , "\n")
print(df.describe() , "\n")


# Parte 2 — Pulizia
# 3. Gestire valori mancanti (es. sostituire con 0, media o metodo più adatto).
#------------------------------------------------------------

#verifico la consistenza e coerenza degli sku su cui mi baso per le imputazioni

df["sku"] = df["sku"].astype(str).str.upper()
pattern_sku = r"^[A-Z0-9]{2}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
mask_sku_ok = df["sku"].astype(str).str.match(pattern_sku, na=False)
tutti_ok = mask_sku_ok.all()
#print("sku ok?", tutti_ok) <-- commento gli output intermedi non richiesti
#sku_non_validi = df.loc[~mask_sku_ok, "sku"].unique()
#print(sku_non_validi)

df["sku"] = df["sku"].astype(str).str.replace(r"^SKU:\s+", "", regex=True)
pattern_sku = r"^[A-Z0-9]{2}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
mask_sku_ok = df["sku"].astype(str).str.match(pattern_sku, na=False)
tutti_ok = mask_sku_ok.all()
#print("sku ok?",tutti_ok)

# pulisco le quantità: individuo i tipi di errore e se si possano correggere (per es str -> int) 
# utilizzo un calcolo predittivo basato sullo sku per le quantità rimaste in N/A 
# verifico e pulisco quelli non ricalcolabili 

pattern_numero = r"^\d+$"
mask_valido = df["quantity"].astype(str).str.match(pattern_numero)
valori_non_numerici = df.loc[~mask_valido, "quantity"].unique()
#print("\nValori non numerici in quantity:") <-- commento gli output intermedi non richiesti
#print(valori_non_numerici  , "\n")

df["quantity"] = df["quantity"].map(lambda x: "0" if x == "zero" else x)
df["quantity"] = df["quantity"].map(lambda x: "10" if x == "10 pezzi" else x)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
mediane_sku = df.groupby("sku")["quantity"].transform("median")  
df["quantity"] = df["quantity"].fillna(mediane_sku)

#print("\n NaN in quantity dopo:")
#print(df["quantity"].isna().sum())
#print("quantity a 0 da droppare:")
#print((df["quantity"] == 0).sum())
df = df.dropna(subset="quantity")
df = df[df["quantity"] > 0]
#print(df.info()) <-- commento gli output intermedi non richiesti

# pulisco il totale: se ho il prezzo dello sku completo il df imputandolo 
# altrimenti droppo gli ordini di cui non idea del prezzo unitario infine cambio valuta 
cambio_rupie = 0.0095

df["item_total"] = (df["item_total"]
                    .astype(str)
                    .str.replace("₹", "")
                    .str.strip()
)
pattern_prezzo = r"^\s*\d+(?:[.,]\d+)?\s*$"
mask_valido = df["item_total"].str.match(pattern_prezzo, na=False)
valori_non_numerici = df.loc[~mask_valido, "item_total"].unique()
#print("\nValori non numerici in item_total:")
#print(valori_non_numerici  , "\n")
pattern_migliaia = r"^\d{1,3}(?:,\d{3})+(?:\.\d+)?$"
mask_migliaia = df["item_total"].notna() & df["item_total"].str.match(pattern_migliaia, na=False)
df.loc[mask_migliaia, "item_total"] = df.loc[mask_migliaia, "item_total"].str.replace(",", "", regex=False)
mask_valido = df["item_total"].str.match(pattern_prezzo, na=False)
valori_non_numerici = df.loc[~mask_valido, "item_total"].unique()
#print("\nValori non numerici in item_total dopo:")
#print(valori_non_numerici  , "\n")
df["item_total"] = pd.to_numeric(df["item_total"], errors="coerce")
#print("\n NaN in item_total da imputare:")
#print(df["item_total"].isna().sum())

df["prezzo_unitario"] = df["item_total"] / df["quantity"]
mediane_prezzo_sku = df.groupby("sku")["prezzo_unitario"].transform("median")  
df["item_total"] = df["item_total"].fillna(mediane_prezzo_sku * df["quantity"])

#print("\n NaN in item_total non imputabili:")
#print(df["item_total"].isna().sum())
df = df.dropna(subset="item_total")
#print(df.info())
df["totale_ordine_euro"] = (df["item_total"]*cambio_rupie).round(2)
#print(df.head())

# 4. Rimuovere duplicati.
# Considero duplicati gli ordini della stessa quantità di oggetti nello stesso momento 
# in quanto è disponibile l'orario preciso
df = df.drop_duplicates(subset=["order_date", "sku", "quantity", "item_total"], keep="first")
#print(df.info())

# 5. Correggere i tipi di dato:
#       - date → datetime
#       - quantità → numeri 
#       - prezzi → float
print("\nMemoria prima dell'ottimizzazione':")
print(df.memory_usage(deep=True).sum())
df["order_date"] = pd.to_datetime(df["order_date"])
df["quantity"] = df["quantity"].astype(int)
df["totale_ordine_euro"] = df["totale_ordine_euro"].astype(float)
df["sku"] = df["sku"].astype("category")
df = df.drop(columns=['prezzo_unitario', 'item_total'])
df.reset_index(drop=True, inplace=True)
print("Memoria dopo:")
print(df.memory_usage(deep=True).sum())

# Parte 3 — Analisi esplorativa
# 6. Calcolare le vendite totali per prodotto.
vendite_prodotto = df.groupby("sku")["totale_ordine_euro"].sum()
print("\nVendite totali in euro per ciascuno sku:")
print(vendite_prodotto)

# 7. Individuare:
#       - il prodotto più venduto
#       - il prodotto meno venduto
quantità_prodotti = df.groupby("sku", observed=True)["quantity"].sum()

prodotto_piu_venduto = quantità_prodotti.idxmax()
print(f"\nProdotto più venduto: {prodotto_piu_venduto}")
prodotto_meno_venduto = quantità_prodotti.idxmin()
print(f"\nProdotto meno venduto: {prodotto_meno_venduto}")

# 8. Calcolare le vendite medie giornaliere.
df["order_day"] = df["order_date"].dt.date
vendite_giornaliere = df.groupby("order_day")["totale_ordine_euro"].sum()

prima_data = df["order_date"].min()
ultima_data = df["order_date"].max()
giorni_totali = (ultima_data - prima_data).days + 1

vendite_medie = (vendite_giornaliere.sum() / giorni_totali).round(2)
print(f"\nVendite medie giornaliere nel periodo di {giorni_totali} giorni: {vendite_medie} €")

# 9. Forecast semplice
# visualizzo l'andamento per individuare un trend
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(vendite_giornaliere.index, vendite_giornaliere.values)
plt.title("Vendite giornaliere nel tempo")
plt.xlabel("Data")
plt.ylabel("Vendite giornaliere (€)")
plt.grid(True)
plt.tight_layout()
plt.show()
#l'andamento delle vendite tra agosto21 e febbraio 22 sembra essere influenzato 
#da una campagna promozionale, calcolo la previsione delle vendite dei prossimi 30 giorni
# basandomi sulla media marzo ottobre 2022
vendite_giornaliere.index = pd.to_datetime(vendite_giornaliere.index)
vendite_stabili = vendite_giornaliere.loc[
    (vendite_giornaliere.index >= "2022-03-01") &
    (vendite_giornaliere.index <= "2022-10-31")
]
baseline_media = vendite_stabili.mean()
ultima_data = vendite_giornaliere.index.max()

date_future = pd.date_range(
    start=ultima_data + pd.Timedelta(days=1),
    periods=30,
    freq="D"
)
baseline_forecast = pd.DataFrame({
    "order_day": date_future,
    "vendite_previste": baseline_media
})
plt.figure(figsize=(12, 5))
plt.plot(vendite_giornaliere.index, vendite_giornaliere.values, label="Storico")
plt.plot(baseline_forecast["order_day"],
         baseline_forecast["vendite_previste"],
         linestyle="--", label="Baseline forecast (30gg)")
plt.legend()
plt.title("Storico vendite e baseline forecast")
plt.xlabel("Data")
plt.ylabel("Vendite (€)")
plt.grid(True)
plt.tight_layout()
plt.show()



