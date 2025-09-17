a = 15
b = 4
print("somma: ", a + b)
print("sottrazione: ", a - b)
print("prodotto: ", a * b)
print("divisione: ", a / b)

import math
x = 8.7
print("Floor: ", math.floor(x))
print("Ceil: ", math.ceil(x))
print("Trunc: ", math.trunc(x))
print("Fabs: ", math.fabs(x))

budget = input("Inserisci il budget: ")
budget = float(budget)
prezzo = input("Inserisci il prezzo: ")
prezzo = float(prezzo)
unita = budget // prezzo
resto = budget % prezzo
print(f"Puoi comprare {unita} unità e ti avanzano {resto} euro")
