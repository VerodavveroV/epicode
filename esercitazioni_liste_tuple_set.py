studenti = {
    'nome' : 'Mario',
    'eta' : 22,
    'corso' : 'Informatica'
}

studenti['eta'] = 23
studenti['matricola'] = '123456'
citta = studenti.get('citta', 'Non specificata')
for chiave, valore in studenti.items():
    print(f"{chiave}: {valore}")

numeri = [12, 7, 9, 18 ,24, 5, 2]
somma_pari = sum([n for n in numeri if n % 2 == 0])
print(f"Somma dei numeri pari: {somma_pari}")

lista = [1, 2, 2, 3, 4, 4, 5]
senza_dup = []
for x in lista:
    if x not in senza_dup:
        senza_dup.append(x)
print(f"lista senza duplicati: {senza_dup}")

lista =[1, 2, 3, 4, 5]
k = 2
rotata = lista[-k:] + lista[:-k]
print(f"Lista rotata: {rotata}")

a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
intersezione = [x for x in a if x in b]
print(f"Intersezione: {intersezione}")

coppie = [('a', 1), ('b', 2), ('c', 3)]
diz = dict(coppie)
print(f"Dizionario da coppie: {diz}")

tuples = [(1,2), (3,4), (5,6)]
somma = sum(sum(t) for t in tuples)
print(f"Somma delle tuple: {somma}")

numeri = [12, 3, 45, 7, 9]
risultato = (min(numeri), max(numeri))
print(f"Minimo e massimo: {risultato}")

