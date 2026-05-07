# Progetto finale — Data Engineering Pipeline (MegaShop)
# Esame pratico: Pandas + Dask + PySpark + Matplotlib/Seaborn

# ---------------------------------------------------------------
# Import
# ---------------------------------------------------------------
import os
import glob
import time

import pandas as pd
import dask.dataframe as dd

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# ---------------------------------------------------------------
# Costanti — percorsi dataset (creati da generator.py)
# ---------------------------------------------------------------
BASE_DIR    = "./data_local"
PARQUET_DIR = os.path.join(BASE_DIR, "parquet")
JSON_DIR    = os.path.join(BASE_DIR, "json")
OUT_DIR     = os.path.join(BASE_DIR, "processed_sales")


# ---------------------------------------------------------------
# ESERCIZIO 1 — Ingestion: Pandas vs Dask
# ---------------------------------------------------------------

# 1.1 Pandas: ciclo for sui file JSON, somma 'amount' per file e totale generale
print("\n=== Esercizio 1.1 — Pandas (file per file) ===")
files = sorted(glob.glob(os.path.join(JSON_DIR, "*.jsonl")))
totale = 0.0
t0 = time.time()
for f in files:
    df = pd.read_json(f, lines=True)
    somma_file = df["amount"].sum()
    print(f"  {os.path.basename(f)}: {somma_file:,.2f}")
    totale += somma_file
print(f"TOTALE GENERALE Pandas: {totale:,.2f}  (in {time.time()-t0:.2f}s)")

# 1.2 Dask: lettura wildcard in un colpo solo + groupby + .compute()
# NOTA: la traccia chiede groupby per 'payment_type' ma quella colonna non
# esiste nei dati generati da generator.py (colonne disponibili:
# transaction_id, customer_id, product_id, region_id, quantity, amount,
# ts, year, month). Uso 'region_id' come proxy categorico.
print("\n=== Esercizio 1.2 — Dask (groupby) ===")
ddf = dd.read_json(os.path.join(JSON_DIR, "*.jsonl"), lines=True, convert_dates=False)
t0 = time.time()
media_per_regione = ddf.groupby("region_id")["amount"].mean().compute()
print("Media 'amount' per region_id:")
print(media_per_regione)
print(f"(calcolato in {time.time()-t0:.2f}s)")


# ---------------------------------------------------------------
# ESERCIZIO 2 — Pipeline ETL con PySpark
# ---------------------------------------------------------------
# E = Extract: leggo le 3 tabelle parquet
# T = Transform: 2 JOIN per arricchire le transazioni con category e region_name
# L = Load: salvo il risultato partizionato per anno

print("\n=== Esercizio 2 — PySpark ETL ===")

# 2.1 SparkSession (singolo entry point per tutto Spark)
spark = (
    SparkSession.builder
    .appName("MegaShop_ETL")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")  # silenzia i log INFO

# 2.2 Extract — fact table + 2 dimension tables
trans_files = glob.glob(os.path.join(PARQUET_DIR, "transactions_batch_*.parquet"))
transazioni = spark.read.parquet(*trans_files)
prodotti    = spark.read.parquet(os.path.join(PARQUET_DIR, "products.parquet"))
regioni     = spark.read.parquet(os.path.join(PARQUET_DIR, "regions.parquet"))

print(f"Transazioni caricate: {transazioni.count():,} righe")
print(f"Prodotti: {prodotti.count():,} righe | Regioni: {regioni.count():,} righe")

# 2.3 Transform — JOIN + select finale
df_clean = (
    transazioni
    .join(prodotti, on="product_id", how="inner")   # aggiunge 'category' e 'price'
    .join(regioni,  on="region_id",  how="inner")   # aggiunge 'region_name'
    .select("transaction_id", "region_name", "category", "amount", "year")
)

print("\nSchema finale:")
df_clean.printSchema()
df_clean.show(5, truncate=False)

# 2.4 Load — Parquet partizionato per anno
(df_clean.write
    .mode("overwrite")          # sovrascrive output esistente
    .partitionBy("year")        # crea sottocartelle year=2020/, year=2021/, ...
    .parquet(OUT_DIR))

print(f"\nOutput salvato in: {OUT_DIR}")


# ---------------------------------------------------------------
# ESERCIZIO 3 — Reporting: Fatturato per Categoria
# ---------------------------------------------------------------
# Pattern: aggrego in Spark (distribuito) -> porto in Pandas il risultato
# aggregato (poche righe, una per categoria) -> grafico con Seaborn.

print("\n=== Esercizio 3 — Reporting fatturato per categoria ===")

# 3.1 Aggregazione in Spark (groupby + sum, ordinato per fatturato decrescente)
fatturato_cat = (
    df_clean
    .groupBy("category")
    .agg(F.sum("amount").alias("fatturato"))
    .orderBy(F.col("fatturato").desc())
)
fatturato_cat.show(truncate=False)

# 3.2 toPandas: trigger dell'esecuzione + materializzazione in memoria locale
pdf = fatturato_cat.toPandas()

# 3.3 Bar chart con Seaborn
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=pdf, x="category", y="fatturato", ax=ax, color="steelblue")

ax.set_title("MegaShop — Fatturato totale per categoria")
ax.set_xlabel("Categoria")
ax.set_ylabel("Fatturato (€)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f} M€"))

# etichetta sopra ogni barra
for bar, valore in zip(ax.patches, pdf["fatturato"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{valore/1e6:.1f} M€", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
out_png = os.path.join(BASE_DIR, "fatturato_per_categoria.png")
plt.savefig(out_png, dpi=120)
print(f"Grafico salvato in: {out_png}")
plt.show()

# 3.4 Chiudo la SparkSession a fine pipeline (libera worker e porte)
spark.stop()
