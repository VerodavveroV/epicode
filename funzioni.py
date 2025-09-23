def quadrato(x):
    return x * x
print(quadrato(5))
print(quadrato(12))

def saluta(nome, saluto="Ciao"):
    return f"{saluto}, {nome}!"
print(saluta("Alice"))
print(saluta("Bob", "Salve"))

def somma(*args):
    return sum(args)
print(somma(1, 2, 3))   
print(somma(10, 20, 30, 40))

def media(*args):
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

print(media(1, 2, 3, 4, 5))

rubrica = {}
def aggiungi_contatto(nome, numero, email=None):
    """aggiunge un contatto alla rubrica"""
    contatto = {"nome" : nome, "numero": numero, "email": email}
    rubrica[nome] = contatto
    print(f"Contatto {nome} aggiunto.")
    return rubrica
def modifica_contatto(nome, nuovo_numero=None, nuovo_email=None):
    """modifica un contatto della rubrica"""
    for contatto in rubrica.values():
        if contatto["nome"].lower() == nome.lower():
            if nuovo_numero:
                contatto["numero"] = nuovo_numero
            if nuovo_email:
                contatto["email"] = nuovo_email
            print(f"Contatto {nome} modificato.")
            return rubrica
    print(f"Contatto {nome} non trovato.")
    return rubrica
def elimina_contatto(nome):
    """elimina un contatto dalla rubrica"""
    for key, contatto in list(rubrica.items()):
        if contatto["nome"].lower() == nome.lower():
            del rubrica[key]
            print(f"Contatto {nome} eliminato.")
            return rubrica
    print(f"Contatto {nome} non trovato.")
    return rubrica  
def cerca_contatto(nome):
    """cerca un contatto nella rubrica"""
    for contatto in rubrica.values():
        if contatto["nome"].lower() == nome.lower():
            print(f"Contatto trovato: Nome: {contatto['nome']}, Numero: {contatto['numero']}, Email: {contatto['email']}")
            return contatto
    print(f"Contatto {nome} non trovato.")
    return None
def mostra_contatti():
    """mostra tutti i contatti della rubrica"""
    if not rubrica:
        print("Rubrica vuota.")
        return
    ordinati = sorted(rubrica.values(), key=lambda x: x['nome'].lower())
    for contatto in ordinati:
        print(f"Nome: {contatto['nome']}, Numero: {contatto['numero']}, Email: {contatto['email']}")
    return rubrica

aggiungi_contatto("Alice", "1234567890")
aggiungi_contatto("Bob", "0987654321","mail@bob.com")
mostra_contatti()
modifica_contatto("Alice", nuovo_email="alice@mail.com")
mostra_contatti()
cerca_contatto("Bob")
elimina_contatto("Alice")
