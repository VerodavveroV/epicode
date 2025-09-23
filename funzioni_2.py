def pulisci_testo(testo):
    """rimuove e pulisce"""
    simboli_da_rimuovere = ['.', ',', '!', '?', ';', ':', '-', '_', '(', ')', '[', ']', '{', '}', '"', "'"]
    for simbolo in simboli_da_rimuovere:
        testo = testo.replace(simbolo, '')
        return testo.lower()
def conta_parole(testo):
    """conta le parole in un testo"""
    parole = testo.split()
    return len(parole)
def frequenza_parole(testo):
    """calcola la frequenza delle parole in un testo"""
    parole = testo.split()
    frequenza_parole = {}
    for parola in parole:
        if parola in frequenza_parole:
            frequenza_parole[parola] += 1
        else:
            frequenza_parole[parola] = 1
    return frequenza_parole
def parole_uniche(testo):
    """restituisce un insieme di parole uniche in un testo"""
    parole = testo.split()
    return set(parole)
def top_n_parole(testo, n=5):
    """restituisce le n parole più frequenti in un testo"""
    frequenza = frequenza_parole(testo)
    parole_ordinate = sorted(frequenza.items(), key=lambda x: x[1], reverse=True)
    return parole_ordinate[:n]
def lunghezza_media_parole(testo):
    """calcola la lunghezza media delle parole in un testo"""
    parole = testo.split()
    if not parole:
        return 0
    lunghezza_totale = sum(len(parola) for parola in parole)
    return lunghezza_totale / len(parole)

testo = "Ciao! Questo è un esempio di testo. Questo testo serve per testare le funzioni di analisi del testo."
testo_pulito = pulisci_testo(testo)
print("Testo pulito:", testo_pulito)
print("Numero di parole:", conta_parole(testo_pulito))
print("Frequenza delle parole:", frequenza_parole(testo_pulito))
print("Parole uniche:", parole_uniche(testo_pulito))
print("Top 5 parole più frequenti:", top_n_parole(testo_pulito, 5))
print("Lunghezza media delle parole:", lunghezza_media_parole(testo_pulito))