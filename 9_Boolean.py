# Esercizio 1 

x = 10 
risultato = x > 0 
print(risultato)


# Esercizio 2

s1 = "ciao mondo"
s2 = "ciao mondo"
print ( s1 == s2 ) 

# Esercizio 3 

a = 5
b = 10 

risultato = (a > 0) and (b > 0)
print(risultato)

#esercizio 4

eta = input("Inserisci la tua età: ")
patente = input("Hai la patente? (sì/no): ")
if (int(eta) >= 18) and (patente.lower() == "sì"):
    puo_guidare = True
else:
    puo_guidare = False
print(puo_guidare)

#esercizio 5
ritardo = input("In ritardo con la consegna? (sì/no): ")
abbonamento = input("Hai un abbonamento premium? (sì/no): ")
if (abbonamento.lower() == "sì"):
    puo_entrare = True
elif (ritardo.lower() == "no"):
    puo_entrare = True
else:
    puo_entrare = False
print(puo_entrare)