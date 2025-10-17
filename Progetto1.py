#Parte 1
titolo = "Il signore degli anelli"
copie_dispo = 3
prezzo_medio = 25.5
disponibile = True
print(titolo)
print(copie_dispo)
print(prezzo_medio)
print(disponibile)
#Parte 2
lista_libri = ["Il Signore degli anelli", "La storia infinita", "Il colore della magia", "Il grande inverno", "La ruota del Tempo"]
archivio_libri = {
    "Titolo" : titolo,
    "Disponiblità" : copie_dispo
}
lista_utenti = set()
#Parte 3
class Libro:
    def __init__(self, titolo, autore, anno, copie_disponibili):
        self.titolo = titolo
        self.autore = autore
        self.anno = anno
        self.copie_disponibili = copie_disponibili
    def info(self):
        return f"\"{self.titolo}\" di {self.autore}, {self.anno}, copie disponibili: {self.copie_disponibili}"
class Utente:
    def __init__(self, nome, eta, id_utente):
        self.nome = nome
        self.eta = eta
        self.id_utente = id_utente
    def scheda(self):
        return f"Utente: {self.nome}, di {self.eta} anni, nr tessera: {self.id_utente}"
class Prestito:
    def __init__(self, utente, libro, giorni):
        self.utente = utente
        self.libro = libro
        self.giorni = giorni
    def dettagli(self):
        return f"L'utente {self.utente.nome} ha noleggiato il libro {self.libro.titolo} per {self.giorni} giorni."
#Parte 4
def presta_libro(utente, libro, giorni):
    if libro.copie_disponibili:
        libro.copie_disponibili -= 1
        nuovo_prestito = Prestito(utente, libro, giorni)
        return nuovo_prestito
    else:
        print("Il libro che cerchi non è disponibile")
        return False
#Test
libro1 = Libro("La storia infinita", "Michael Ende", 1981, 2) 
print(libro1.info())
libro2 = Libro("Il Signore degli Anelli", " John R. R. Tolkien ", 1977, 1)
libro3 = Libro("L'angelo della finestra d'Occidente", "Gustav Meyrink", 1927, 2)
utente1 = Utente("Luca", 16, 187)
print(utente1.scheda())
utente2 = Utente("Anna", 22, 321)
utente3 = Utente("Maria", 87, 100)
prestito1 = presta_libro(utente1, libro1, 15)
prestito2 = presta_libro(utente2, libro2, 10)
prestito3 = presta_libro(utente3, libro3, 20)
prestito_no = presta_libro(utente3, libro2, 10)
print(f"copie disponibili di {libro1.titolo}: {libro1.copie_disponibili}")
print(f"copie disponibili di {libro2.titolo}: {libro2.copie_disponibili}")
print(f"copie disponibili di {libro3.titolo}: {libro3.copie_disponibili}")
print(prestito1.dettagli())
print(prestito2.dettagli())
print(prestito3.dettagli())


