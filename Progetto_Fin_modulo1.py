import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Parte1
negozi = ["Milano", "Roma", "Napoli", "Torino", "Bologna"]
prodotti = ["Smartphone", "Laptop", "TV", "Tablet", "Cuffie"]
date = pd.date_range(start="2025-10-01", periods=30, freq="D").strftime("%Y-%m-%d")
dati = []
for i in range(35):
    data = np.random.choice(date)
    negozio = str(np.random.choice(negozi))
    prodotto = str(np.random.choice(prodotti))
    quantita = np.random.randint(1, 10)
    prezzo_unitario = round(np.random.uniform(10.00, 1000.00), 2)
    dati.append([data, negozio, prodotto, quantita, prezzo_unitario])
df_gen = pd.DataFrame(dati, columns=["Data", "Negozio", "Prodotto", "Quantita", "Prezzo unitario"])
#df_gen.to_csv("vendite.csv")
#Parte2
df = pd.read_csv("vendite.csv")
print("Prime 5 righe del dataset:")
print(df.head())
print("\nNumero di righe e colonne del dataset:")
print(df.shape)
print("\nFormato del dataset:")
print(df.info())
#Parte3
df["Incasso"] = df["Quantita"] * df["Prezzo unitario"]
incasso_catena = df["Incasso"].sum()
incassi_negozi = (
    df.groupby("Negozio")["Incasso"]
      .mean()
      .round(2)
      .reset_index(name="Incasso medio")
      .sort_values("Incasso medio", ascending=True)
)
print(f"\nL'incasso totale della catena di negozi è {incasso_catena} €")
print("\nL'incasso medio per negozio in euro è:")
print(incassi_negozi)
print(f"\n I tre prodotti più venduti e la relativa quantità sono: \n{df["Prodotto"].value_counts().head(3).to_string()}")
incassi_negozi_prodotti = (
    df.groupby(["Negozio", "Prodotto"])["Incasso"]
      .mean()
      .round(2)
      .reset_index(name="Incasso medio per prodotto")
      .sort_values(["Negozio", "Incasso medio per prodotto"], ascending=[True,False])
)
print(f"\nPer i negozi i prodotti hanno generato in media questo incasso in €: \n {incassi_negozi_prodotti}")
#Parte4
a = (df["Quantita"]).to_numpy()
print(f"\nIl numero medio di oggetti acquistati è: {np.mean(a):.2f}")
print(f"La quantità massima è: {np.max(a):.2f}")
print(f"La quantità minima è: {np.min(a):.2f}")
print(f"La deviazione standard tra le quantità è: {np.std(a):.2f}")
media = np.mean(a)
sopra_media = np.sum(a > media) / len(a) * 100
print(f"Gli acquisti con quantità sopra la media sono il {sopra_media:.2f}% del totale")
b = df[["Quantita", "Prezzo unitario"]].to_numpy()
incasso_np = sum(b[:,0] * b[:,1])
print(f"Il totale calcolato in precedenza pari a {incasso_catena:.2f} corrisponde a {incasso_np:.2f}")
#Parte5
risultati_negozi = df.groupby("Negozio")["Incasso"].sum()
risultato_medio_negozio = risultati_negozi.mean()
df.groupby("Negozio")["Incasso"].sum().plot(kind="bar", color="#D81159")
plt.title("Incasso in € per negozio", fontsize=14, color="#218380")
plt.axhline(y=risultato_medio_negozio, color='#73D2DE', linestyle='--', linewidth=2, label="Media")
plt.legend()
plt.show()
colors =["#D81159", "#8F2D56", "#218380", "#FBB13C", "#73D2DE", "#D6FFB7"]
df.groupby("Prodotto")["Incasso"].sum().plot(kind="pie",labels=df["Prodotto"], autopct="%1.0f%%", colors=colors[:len(df)])
plt.title("Incidenza percentuale dei prodotti sugli incassi")
plt.show()
df.groupby("Data")["Incasso"].sum().plot(kind="line", marker='d', color="#D81159")
plt.title("Incassi per giorno in €", fontsize=14, color="#218380")
plt.show()
#Parte6
df_cat = df.copy()
#print(set(df["Prodotto"]))
categorie = {
    'Smartphone' : "Telefonia",
    'Laptop' : "Informatica",
    'Cuffie' : "Informatica", 
    'Tablet' : "Informatica", 
    'TV' : "Elettronica"
}
df_cat["Categoria"] = df_cat["Prodotto"].map(categorie)
df_cat1 = (
    df_cat.groupby("Categoria")
      .agg({
          "Incasso" : "sum",
          "Quantita" : "mean"
      })
      .reset_index()
      .rename(columns = {
          "Incasso" : "Incasso Categoria",
          "Quantita" : "Nr medio di prodotti venduti"
      })
      .round(2)
)
df_cat1.to_csv("vendite_analizzate.csv")
#Parte7
df_cat2 = (df_cat.groupby("Categoria")
      .agg({
          "Incasso" : "mean",
          "Quantita" : "mean"
      })
      .reset_index()
      .rename(columns = {
          "Incasso" : "Incasso medio",
          "Quantita" : "Quantità media"
      })
)
fig, ax1 = plt.subplots()
bar = ax1.bar(df_cat2["Categoria"], df_cat2["Incasso medio"], color="#D81159")
ax2 = ax1.twinx()
ax2.plot(df_cat2["Categoria"], df_cat2["Quantità media"], color="#218380", marker="o", linewidth=2)
plt.title("Incassi e quantità media per categoria", fontsize=14)
ax1.set_ylabel("Incasso medio €")
ax2.set_ylabel("Quantità media")
plt.show()

def top_n_prodotti(n):
    df_top = (
        df.groupby("Prodotto")["Incasso"]
          .sum()
          .reset_index(name="Incasso totale prodotto")
          .sort_values("Incasso totale prodotto", ascending=False)
    )
    return f"\nI {n} prodotti che hanno generato più incasso sono: \n {df_top.head(n)}"
print(top_n_prodotti(7))