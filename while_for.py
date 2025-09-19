num = float(input("Inserisci un numero positivo: "))
while num <0:
    num = float(input("Inserisci un numero positivo: "))
else:
    print(f"Hai inserito il numero positivo: {num}")

i = 1
while i <= 5:
    print(i)
    i += 1  

i = 2
while i <= 10:
    print(i)
    i += 2

i = 1
somma = 0
while i <= 10:
    somma += i
    i += 1
print(f"somma = : {somma}")

n = 7
i = 1
while i <= 10:
    print(f"{n} x {i} = {n*i}")
    i += 1

somma = 0
n = int(input("Inserisci un numero (0 per uscire): "))
while n != 0:
    somma += n
    n = int(input("Inserisci un numero (0 per uscire): "))
print(f"Somma totale: {somma}")

segreto = 7
tentativo = int(input("Indovina il numero segreto (tra 1 e 10): "))
while tentativo != segreto:
    tentativo = int(input("Sbagliato! Riprova: "))
print("Hai indovinato!")

i = 1
while i <= 15:
    print(i)
    i += 2

#esercizio: calcolare la somma delle cifre di un numero
num = int(input("Inserisci un numero intero positivo: "))
somma_cifre = 0
while num > 0:
    cifra = num % 10
    somma_cifre += cifra
    num //= 10
print(f"La somma delle cifre è: {somma_cifre}")

lista_nomi = ['Alice', 'Bob', 'Charlie', 'David']
for i, nome in enumerate(lista_nomi):
    print(i, nome)

for i in range(1, 11):
    print(i)

for i in range(2, 21, 2):
    print(i)

parola = "Python"
for c in parola:
    print(c)

somma = 0
for i in range(1, 101):
    somma += i
print(somma)

for i in range(1, 11):
    print(f"5 x {i} = {5*i}")

n = 5
fattoriale = 1
for i in range(1, n + 1):
    fattoriale *= i 
print(f"Il fattoriale di {n} è {fattoriale}")

parola = 'programmazione'
vocali = 'aeiou'
conta = 0
for c in parola:
    if c in vocali:
        conta += 1
print(f"La parola '{parola}' contiene {conta} vocali.")

for i in range (1, 4):
    for j in range(1, 4):
        print(i, j , end= "  ")
    print()

for i in range (1, 11):
    if i == 5:
        continue
    print(i)

for i in range (1, 11):
    if i == 8:
        break
    print(i)


   