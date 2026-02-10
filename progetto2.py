# ============================================================
# PROGETTO #2 — ANALISI VENDITE REALISTICA
# ============================================================
#
# Contesto:
# Sei un data analyst in un’azienda e-commerce.
# Devi integrare più fonti dati (CSV, JSON),
# ottimizzare memoria, creare colonne derivate,
# applicare filtri e aggregazioni.
#
# ============================================================
# ------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------
import pandas as pd
import numpy as np

# ============================================================
# PARTE 1 — CREAZIONE DEI DATASET
# ============================================================

# ------------------------------------------------------------
# 1) CREAZIONE ordini.csv
# ------------------------------------------------------------
# - 100.000 righe
# - colonne:
#     * ClienteID
#     * ProdottoID
#     * Quantità
#     * DataOrdine
#
# Obiettivo:
# - simulare ordini clienti realistici
# - salvare il dataset in formato CSV
# TODO:
# - generare array di ClienteID
# - generare array di ProdottoID
# - generare quantità casuali
# - generare date ordine
# - creare DataFrame
# - salvare in ordini.csv

date_possibili = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    freq="D"
)

ordini = pd.DataFrame({
    "ClienteID" : np.random.randint(1, 50, size= 100_000),
    "ProdottoID" : np.random.randint(1, 21, size=100_000),
    "Quantità" : np.random.randint(1, 6, size=100_000),
    "DataOrdine": np.random.choice(date_possibili, size=100_000)
})

ordini.to_csv("ordini.csv", index=False)

# ------------------------------------------------------------
# 2) CREAZIONE prodotti.json
# ------------------------------------------------------------
# - 20 prodotti
# - colonne:
#     * ProdottoID
#     * Categoria
#     * Fornitore
#     * Prezzo
#
# Obiettivo:
# - simulare anagrafica prodotti
# - salvare in formato JSON
# - TODO:
# - creare lista di prodotti
# - assegnare categoria e fornitore
# - creare DataFrame
# - salvare in prodotti.json

categorie = ["Propulsione", "Avionica", "Difesa", "Supporto Vitale", "Armamenti"]

categoria_fornitore = { "Propulsione": "HyperDrive Corp",
                        "Avionica" : "Stellar Dynamics",
                        "Difesa" : "CosmoShield Systems",
                        "Supporto Vitale" : "VoidWorks Engineering",
                        "Armamenti" : "NovaTech Industries"
}

prodotti = pd.DataFrame({
    "ProdottoID" : np.arange(1, 21),
    "Categoria" : np.random.choice(categorie, size=20),
    "Prezzo" : np.random.randint(100, 5_000, size=20)
})
prodotti["Fornitore"] = prodotti["Categoria"].map(categoria_fornitore)

#print(prodotti.head())
#print(prodotti.info())

prodotti.to_json("prodotti.json", orient="records")
# ------------------------------------------------------------
# 3) CREAZIONE clienti.csv
# ------------------------------------------------------------
# - 5.000 clienti
# - colonne:
#     * ClienteID
#     * Regione
#     * Segmento
#
# Obiettivo:
# - simulare base clienti
# - salvare in formato CSV
# TODO:
# - generare ClienteID
# - assegnare regione e segmento
# - creare DataFrame
# - salvare in clienti.csv
regioni = ["Andromeda", "Orione", "Esterni", "Aquila"]

clienti = pd.DataFrame({
    "ClienteID" : np.arange(1, 5_001),
    "Regione" : np.random.choice(regioni, size=5_000),
    "Segmento" : np.random.choice(["vip", "citizen", "robot"])
})
#print(clienti.head())
#print(clienti.info())

clienti.to_csv("clienti.csv", index=False)
# ============================================================
# PARTE 2 — CREAZIONE DATAFRAME UNIFICATO
# ============================================================

# ------------------------------------------------------------
# 4) LETTURA ordini.csv
# ------------------------------------------------------------
# - caricare il file CSV ordini
# - verificare struttura e tipi di dato
df_ordini = pd.read_csv("ordini.csv")
print("\nordini:\n",df_ordini.head())
print(df_ordini.info())

# ------------------------------------------------------------
# 5) LETTURA prodotti.json
# ------------------------------------------------------------
# - caricare il file JSON prodotti
# - verificare struttura
df_prodotti = pd.read_json("prodotti.json")
print("\nprodotti:\n", df_prodotti.head())
print(df_prodotti.info())

# ------------------------------------------------------------
# 6) LETTURA clienti.csv
# ------------------------------------------------------------
# - caricare il file CSV clienti
df_clienti = pd.read_csv("clienti.csv")
print("\nclienti:\n", df_clienti.head())
print(df_clienti.info())

# ------------------------------------------------------------
# 7) MERGE DEI DATASET
# ------------------------------------------------------------
# - unire:
#     * ordini + prodotti (su ProdottoID)
#     * risultato + clienti (su ClienteID)
#
# Obiettivo:
# - ottenere un DataFrame unico con:
#   ordini + info prodotto + info cliente

df_i = df_ordini.merge(df_prodotti, on="ProdottoID", how="left")
df = df_i.merge(df_clienti, on="ClienteID", how="left")

print("\ndatabase completo:\n", df.info())
print(df.head())
# ============================================================
# PARTE 3 — OTTIMIZZAZIONE
# ============================================================

# ------------------------------------------------------------
# 8) OTTIMIZZAZIONE TIPI DI DATO
# ------------------------------------------------------------
# - convertire:
#     * stringhe ripetute in category
#     * ID in int32 / int16 se possibile
#     * date in datetime
#
# Obiettivo:
# - ridurre uso memoria



mem_prima = df.memory_usage(deep=True).sum()
print("\nMemoria prima (byte):", mem_prima)
print("Memoria prima (MB):", mem_prima / 1024**2)

df["ClienteID"] = df["ClienteID"].astype("int16")
df["ProdottoID"] = df["ProdottoID"].astype("int16")
df["Quantità"] = df["Quantità"].astype("int16")
df["DataOrdine"] = pd.to_datetime(df["DataOrdine"])
df["Prezzo"] = df["Prezzo"].astype("float32")
df["Categoria"] = df["Categoria"].astype("category")
df["Fornitore"] = df["Fornitore"].astype("category")
df["Regione"] = df["Regione"].astype("category")
df["Segmento"] = df["Segmento"].astype("category")

# ------------------------------------------------------------
# 9) ANALISI USO MEMORIA
# ------------------------------------------------------------
# - misurare memoria prima e dopo
# - confrontare i risultati

mem_dopo = df.memory_usage(deep=True).sum()
print("Memoria dopo (byte):", mem_dopo)
print("Memoria dopo (MB):", mem_dopo / 1024**2)

saved_bytes = mem_prima - mem_dopo
saved_mb = saved_bytes / 1024**2

print("\nRisparmio memoria (byte):", saved_bytes)
print("Risparmio memoria (MB):", saved_mb)
print("Riduzione (%):", (saved_bytes / mem_prima) * 100)

# ============================================================
# PARTE 4 — COLONNE DERIVATE E FILTRI
# ============================================================
# ------------------------------------------------------------
# 10) CREAZIONE COLONNA DERIVATA
# ------------------------------------------------------------
# - ValoreTotale = Prezzo * Quantità
#
# Nota:
# - colonna fondamentale per analisi revenue

df["ValoreTotale"] = df["Prezzo"]*df["Quantità"]

# ------------------------------------------------------------
# 11) FILTRI AVANZATI
# ------------------------------------------------------------
# - filtrare:
#     * ordini con ValoreTotale > 100 (modificato in > 10_000 per via del db)
#     * clienti appartenenti a specifici segmenti / regioni
#
# Nota:
# - usare .copy() dopo il filtro
#   per evitare SettingWithCopyWarning

subset_top_ordini = df[df["ValoreTotale"] > 10_000].copy()
print("\nPrime righe del subset top ordini:\n", subset_top_ordini.head())

subset_clienti_robot = df[df["Segmento"] == "robot"].copy()
print("\nPrime righe del subset clienti robot:\n", subset_clienti_robot.head())


# ============================================================
# (EVENTUALE ESTENSIONE)
# ============================================================
# - aggregazioni per:
#     * Regione
#     * Categoria
#     * Segmento
# - serializzazione efficiente (Parquet / HDF5)
# - confronto performance
#
# ============================================================
df.set_index(["Regione", "Categoria", "Segmento"], inplace=True)

report = df.groupby(level=["Regione", "Categoria", "Segmento"]).agg(
    totale_vendite=pd.NamedAgg(column="ValoreTotale", aggfunc="sum"),
    media_quantità=pd.NamedAgg(column="Quantità", aggfunc="mean")
)
report = report.reset_index()
print("\nPrime righe del report:\n")
print(report.head())

import time

report.to_parquet("report.parquet")
report.to_hdf("report.h5", key="report", mode="w", format="table")
report.to_csv("report.csv", index=False)

start = time.time()
pd.read_csv("report.csv")
print("\nTempo lettura CSV:", time.time() - start)

start = time.time()
pd.read_parquet("report.parquet")
print("Tempo lettura Parquet:", time.time() - start)


start = time.time()
pd.read_hdf("report.h5", key="report")
print("Tempo lettura HDF5:", time.time() - start)
