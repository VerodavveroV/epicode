import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Parte1
nome = "Mario Rossi"
eta = int(34)
saldo_conto = float(2500.60)
stato_VIP = bool(True)
destinazioni = ["Roma", "Firenze", "Venezia", "Palermo", "Torino"]
prezzo_destinazione = {
    "Roma" : 500,
    "Firenze" : 350,
    "Venezia" : 800,
    "Palermo" : 1.200,
    "Torino" : 400
}
#Parte2
class Cliente:
    def __init__(self, nome, eta, vip):
        self.nome = nome
        self.eta = eta
        self.vip = vip
    def __str__(self):
        if self.vip:
            status = "è un VIP"
        else:
            status = "non è un VIP"
        return f"Il cliente {self.nome}, di {self.eta} anni, {status}"
class Viaggio:
    def __init__(self, destinazione, prezzo, durata):
        self.destinazione = destinazione
        self.prezzo = prezzo
        self.durata = durata
class Prenotazione:
    def __init__(self, cliente, viaggio):
        self.cliente = cliente
        self.viaggio = viaggio
    def prezzo_viaggio(self):
        if self.cliente.vip:
            return self.viaggio.prezzo * self.viaggio.durata * 0.9
        else:
            return self.viaggio.prezzo * self.viaggio.durata
    def dettagli(self):
        return f"Il cliente {self.cliente.nome} ha prenotato un viaggio di {self.viaggio.durata} giorni a {self.viaggio.destinazione} al costo di {self.prezzo_viaggio():.2f} €."
#Parte3
np.random.seed(42)
prenotazioni = np.array(np.random.randint(200, 2001, 100))
print("Il prezzo medio delle prenotazioni è: ", np.mean(prenotazioni), "€")
print("La prenotazione più costosa è: ", np.max(prenotazioni), "€")
print("La prenotazione meno costosa è: ", np.min(prenotazioni), "€")
print("La deviazione standard tra i prezzi è: ", np.std(prenotazioni))
media = np.mean(prenotazioni)
sopra_media = np.sum(prenotazioni > media) / len(prenotazioni) * 100
print(f"Le prenotazioni sopra la media sono il {sopra_media}% del totale")
#Parte4
np.random.seed(42)
dati = {
    "Cliente": [
        "Mario Rossi", "Lucia Bianchi", "Anna Verdi", "Giovanni Neri", "Paolo Gialli",
        "Chiara Blu", "Laura Rosa", "Andrea Grigi", "Elena Viola", "Stefano Nero"
    ],
    "Destinazione": [
        "Roma", "Parigi", "Roma", "Tokyo", "Roma",
        "Parigi", "Madrid", "Atene", "Atene", "Amsterdam"
    ],
    "Prezzo": list(np.random.randint(200, 2001, 10)),
    "Giorno_partenza": [
        "2025-06-10", "2025-06-12", "2025-06-15", "2025-06-20", "2025-06-22",
        "2025-06-25", "2025-06-27", "2025-06-29", "2025-07-01", "2025-07-03"
    ],
    "Durata": list(np.random.randint(2, 8, 10))
}
df = pd.DataFrame(dati)
incasso_totale = sum(df["Prezzo"])
print(f"L'incasso totale dell'agenzia nel periodo è {incasso_totale:.2f} €")
incasso_m_destinazione = df.groupby("Destinazione")["Prezzo"].mean().round(2)
print(f"L'incasso medio per ogni destinazione è:") 
print(f"{incasso_m_destinazione.to_string()}")
print(f"Le tre destinazioni più frequenti sono:")
print(f"{df["Destinazione"].value_counts().head(3).to_string()}")
#Parte 5
#print(df)
df_bar = (
    df.groupby("Destinazione")["Prezzo"]
      .sum()
      .reset_index(name="Incassi_tot")
      .sort_values("Incassi_tot", ascending=True)
)
#print(df_bar)
media_incassi_tot = df_bar["Incassi_tot"].mean()
plt.barh(df_bar["Destinazione"], df_bar["Incassi_tot"], color="#D81159")
plt.title("Distribuzione incassi per destinazione", fontsize=14, color="#218380")
plt.xlabel("Incasso (€)")
plt.axvline(x=media_incassi_tot, color='#73D2DE', linestyle='--', linewidth=2, label="Media")
plt.legend()
plt.show()

media_incasso =df["Prezzo"].mean()
df["Giorno_partenza"] = pd.to_datetime(df["Giorno_partenza"])
plt.plot(df["Giorno_partenza"], df["Prezzo"], marker='d', color="#D81159")
plt.title("Incassi per giorno di partenza", fontsize=14, color="#218380")
plt.xlabel("Partenza", color="#8F2D56")
plt.ylabel("Incasso in €", color="#8F2D56")
plt.axhline(y=media_incasso, color='#73D2DE', linestyle='--', linewidth=2, label="Media")
plt.legend()
plt.show()

colors =["#D81159", "#8F2D56", "#218380", "#FBB13C", "#73D2DE", "#D6FFB7"]
plt.pie(df_bar["Incassi_tot"], labels=df_bar["Destinazione"], autopct="%1.0f%%", colors=colors[:len(df_bar)])
plt.title("Incidenza percentuale delle destinazioni")
plt.show()
#Parte 6
np.random.seed(42)
dati_viaggi_mondo = {
    "Cliente": [
        "Mario Rossi", "Lucia Bianchi", "Elena Viola", "Giovanni Neri", "Mario Rossi",
        "Chiara Blu", "Mario Rossi", "Andrea Grigi", "Elena Viola", "Lucia Bianchi"
    ],
    "Destinazione": [
        "Roma", "Parigi", "Manila", "Tokyo", "Nairobi",
        "Parigi", "Madrid", "Tunisi", "Atene", "New York"
    ],
    "Prezzo": list(np.random.randint(200, 2001, 10)),
    "Giorno_partenza": [
        "2025-06-10", "2025-06-12", "2025-06-15", "2025-06-20", "2025-06-22",
        "2025-06-25", "2025-06-27", "2025-06-29", "2025-07-01", "2025-07-03"
    ],
    "Durata": list(np.random.randint(2, 18, 10))
}
df_mondo = pd.DataFrame(dati_viaggi_mondo)
categorie_dest = {
    "Roma" : "Europa",
    "Parigi" : "Europa",
    "Manila" : "Asia", 
    "Tokyo" : "Asia",
    "Nairobi" : "Africa",
    "Parigi" : "Europa",
    "Madrid" : "Europa", 
    "Tunisi" : "Africa",
    "Atene" : "Europa",
    "New York" : "America"
}
df_mondo["Continente"] =df_mondo["Destinazione"].map(categorie_dest)
df_mondo1 = (
    df_mondo.groupby("Continente")
      .agg({
          "Prezzo" : "sum",
          "Durata" : "mean"
      })
      .reset_index()
      .rename(columns = {
          "Prezzo " : "Incassi_Continente",
          "Durata" : "Durata_media_Continente"
      })
)
df_mondo1.to_csv("prenotazioni_analizzate.csv")
#Parte7
def clienti_vip(lista_prenotazioni, requisito_vip):
    requisito_vip = int(requisito_vip)
    lista_clienti_vip = []
    for cliente in set(lista_prenotazioni):
        nr_prenotazioni = lista_prenotazioni.count(cliente)
        if nr_prenotazioni >= requisito_vip:
            lista_clienti_vip.append(cliente)
    return print(lista_clienti_vip)
df_mondo2 = (df_mondo.groupby("Continente")
      .agg({
          "Prezzo" : "mean",
          "Durata" : "mean"
      })
      .reset_index()
      .rename(columns = {
          "Prezzo" : "Incasso medio",
          "Durata" : "Durata media"
      })
)
#print(df_mondo2)
fig, ax1 = plt.subplots()
bar = ax1.bar(df_mondo2["Continente"], df_mondo2["Incasso medio"], color="#D81159")
ax2 = ax1.twinx()
ax2.plot(df_mondo2["Continente"], df_mondo2["Durata media"], color="#218380", marker="o", linewidth=2)
plt.title("Incassi e durata media per continente", fontsize=14)
plt.show()
#test
#cliente1 = Cliente("Mario Rossi", 34, True)
#print(cliente1)
#viaggio1 = Viaggio("Roma", 500, 2)
#prenotazione1 = Prenotazione(cliente1, viaggio1)
#print(prenotazione1.dettagli())
#cliente = [
#        "Mario Rossi", "Lucia Bianchi", "Elena Viola", "Giovanni Neri", "Mario Rossi",
#        "Chiara Blu", "Mario Rossi", "Andrea Grigi", "Elena Viola", "Lucia Bianchi"]
#clienti_vip(cliente, 2)
