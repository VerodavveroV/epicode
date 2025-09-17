x = -10
if x >= 0:
    print("positivo")
else:
    print("negativo")

a = 10
b = 7
if a > b:
    print("a è maggiore di b")
else:
    print("b è maggiore di a")

età = 20
if età >= 18:
    print("sei maggiorenne")
else:
    print("sei minorenne")

eta = 12
eta = int(eta)
if eta < 18:
    print("sei minorenne")
elif eta >= 18 and eta < 65:
    print("sei adulto")
else:
    print("sei anziano")

n = 9
if n % 3 == 0:
    print("il numero inserito è multiplo di 3")
else:
    print("il numero inserito non è multiplo di 3")

voto = 22
if voto >= 18:
    print("il voto è sufficiente, ESAME SUPERATO!")
else:
    print("il voto non è sufficiente, BOCCIATO")

c = "a"
if c in "aeiou":
    print("vocale")
else:
    print("consonante")

n = 0
if n > 0:
    print("positivo")
elif n < 0:
    print("negativo")
else:
    print("zero")

a, b, c = 7, 3, 9
if a >= b and a >= c:
    print("a è il maggiore dei tre numeri")
elif a <= b and c <= b:
    print("b è il maggiore dei tre numeri")
else:
    print("c è il maggiore dei tre numeri")

eta = 70
if eta < 12:
    prezzo = 5
elif eta < 65:
    prezzo = 10
else:
    prezzo = 7
print(f"Il prezzo del biglietto è: {prezzo} euro")

a, b, c = 5, 5, 3
if a == b == c:
    print("il triangolo è equilatero")
elif a == b or b == c or a == c:
    print("il triangolo è isoscele")
else:
    print("il triangolo è scaleno")

