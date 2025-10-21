import numpy as np
#Parte1
p1_nome = str("Luca")
p1_cognome = str("Bianchi")
p1_codice_fiscale = str("BNCLCU85A01F205Z")
p1_eta = int(39)
p1_peso = float(78.5)
p1_analisi =["glicemia","ematocrito","colesterolo"]
p2_nome = str("Giulia")
p2_cognome = str("Rossi")
p2_codice_fiscale = str("RSSGLI97C65L219P")
p2_eta = int(28)
p2_peso = float(62)
p2_analisi = ["glicemia","immunoglobuline","leucociti"]
p3_nome = str("Marco")
p3_cognome = str("Verdi")
p3_codice_fiscale = str("VRDMRC73E12M345N")
p3_eta = int(52)
p3_peso = float(84.3)
p3_analisi = ["transaminasi","piastrine","emoglobina"]


#Parte2
class Paziente:
    def __init__(self, nome, cognome, codice_fiscale, eta, peso, analisi_effettuate):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.eta = eta
        self.peso = peso
        self.analisi_effettuate = analisi_effettuate
    def scheda_personale(self):
        return f"Paziente: {self.nome} {self.cognome}, codice fiscale: {self.codice_fiscale}, di anni {self.eta} e peso {self.peso}, \n analisi effettuate per Glicemia, Colesterolo ed Emoglobina: \n{self.analisi_effettuate}"


#Parte4
    def statistiche_analisi(self):
        analisi = self.analisi_effettuate
        glicemia = analisi[:,0]
        colesterolo = analisi[:,1]
        emoglobina = analisi[:,2]
        return f"Paziente: {self.nome} {self.cognome}\nGlicemia media: {np.mean(glicemia)}, massima: {np.max(glicemia)}, minima: {np.min(glicemia)}. Deviazione standard: {np.std(glicemia):.2f}\nColesterolo medio: {np.mean(colesterolo)}, massimo: {np.max(colesterolo)}, minimo: {np.min(colesterolo)}. Deviazione standard: {np.std(colesterolo):.2f}\nEmoglobina media: {np.mean(emoglobina)}, massima: {np.max(emoglobina)}, minima: {np.min(emoglobina)}. Deviazione standard: {np.std(emoglobina):.2f}"


paziente1 = Paziente("Luca","Bianchi","BNCLCU85A01F205Z",39,78.5,p1_analisi)
paziente2 = Paziente("Giulia","Rossi","RSSGLI97C65L219P",28,62.0,p2_analisi)
paziente3 = Paziente("Marco","Verdi","VRDMRC73E12M345N",52,84.3,p3_analisi)
#test
#print(paziente2.scheda_personale())
class Medico:
    def __init__(self, nome, cognome, specializzazione):
        self.nome = nome
        self.cognome = cognome
        self.specializzazione = specializzazione
    def visita_paziente(self, paziente):
        return f"Il dottore in {self.specializzazione}, {self.nome} {self.cognome}, sta visitando {paziente.nome} {paziente.cognome}."
medico1 = Medico("Antonio","Sangue","Ematologia")
#test
#print(medico1.visita_paziente("paziente1"))
class Analisi:
    def __init__(self, tipo_analisi):
        self.tipo_analisi = tipo_analisi
        self.esito = None
    def valuta(self, paziente):
        """aggiunto codice per importare gli array dei risultati"""     
        """viene valutata la media degli esami dell'array"""
        mappa_esami = {
            "glicemia": 0,
            "colesterolo": 1,
            "emoglobina": 2, 
        }
        col = mappa_esami[self.tipo_analisi]
        self.esito = float(np.mean(paziente.analisi_effettuate[:, col]))
        if self.tipo_analisi == "glicemia":
            if self.esito < 70 or self.esito > 99:
                return f"Paziente {paziente.nome} {paziente.cognome} - Glicemia: valore medio anomalo"
            else:
                return f"Paziente {paziente.nome} {paziente.cognome} - Glicemia: valore medio nel range di riferimento"
        if self.tipo_analisi == "ematocrito":
            if self.esito < 36 or self.esito > 52:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "colesterolo":
            if self.esito > 200:
                return f"Paziente {paziente.nome} {paziente.cognome}- Colesterolo: valore medio anomalo"
            else:
                return f"Paziente {paziente.nome} {paziente.cognome} - Colesterolo: valore medio nel range di riferimento"
        if self.tipo_analisi == "immunoglobuline":
            if self.esito < 700 or self.esito > 1600:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "leucociti":
            if self.esito < 4 or self.esito > 10:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "transaminasi":
            if self.esito < 7 or self.esito > 56:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "ematocrito":
            if self.esito < 7 or self.esito > 56:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "piastrine":
            if self.esito < 150 or self.esito > 400:
                return "valore anomalo"
            else:
                return "valore nel range di riferimento"
        if self.tipo_analisi == "emoglobina":
            if self.esito < 12 or self.esito > 17:
                return f"Paziente {paziente.nome} {paziente.cognome} - Emoglobina: valore anomalo"
            else:
                return f"Paziente {paziente.nome} {paziente.cognome} - Emoglobina: valore nel range di riferimento"
#test
#analisi1 = Analisi("glicemia", 25)
#analisi2 = Analisi("ematocrito", 40)
#print(Analisi.valuta(analisi1))
#print(Analisi.valuta(analisi2))


#Parte 3
lista_risultati_analisi = [11.8, 12.5, 13.2, 13.9, 14.4, 14.8, 15.1, 15.7, 16.3, 17.1]
emoglobina = np.array(lista_risultati_analisi)
media = np.mean(emoglobina)
valore_massimo = np.max(emoglobina)
valore_minimo = np.min(emoglobina)
deviazione_standard = np.std(emoglobina)
#test
#print(emoglobina)
#print(media)
#print(valore_massimo)
#print(valore_minimo)
#print(deviazione_standard)


#Parte4:
"""array in cui le righe sono i giorni di analisi e le colonne sono glicemia, colesterolo, emoglobina"""
analisi = np.array([
    [95, 185, 13.5],
    [100, 195, 13.2],
    [88, 178, 12.9],
    [110, 205, 14.2],
    [99, 190, 13.7]
])
glicemia = analisi[:,0]
colesterolo = analisi[:,1]
emoglobina = analisi[:,2]
#test
#print(glicemia)
#print(colesterolo)
#print(emoglobina)
#test
#analisi_p1 = np.array([
#    [95, 185, 13.5],
#    [100, 195, 13.2],
#    [88, 178, 12.9],
#    [110, 205, 14.2],
#    [99, 190, 13.7]
#])
#paziente1 = Paziente("Luca","Bianchi","BNCLCU85A01F205Z",39,78.5,analisi_p1)
#print(paziente1.statistiche_analisi())


#Parte 5
def main():
    analisi_p1 = np.array([
    [95, 185, 13.5],
    [100, 195, 13.2],
    [88, 178, 12.9],
    [110, 205, 14.2],
    [99, 190, 13.7]
    ])
    analisi_p2 = np.array([
    [85, 170, 12.8],
    [92, 175, 13.0],
    [97, 182, 13.4],
    [90, 168, 12.7],
    [94, 180, 13.1]
    ])
    analisi_p3 = np.array([
    [105, 210, 14.6],
    [112, 220, 14.8],
    [108, 215, 14.5],
    [115, 225, 14.9],
    [110, 218, 14.7]
    ])
    analisi_p4 = np.array([
    [90, 175, 12.5],
    [92, 180, 12.7],
    [88, 172, 12.3],
    [95, 185, 12.8],
    [91, 178, 12.6]
    ])
    analisi_p5 = np.array([
    [115, 220, 13.8],
    [120, 230, 13.5],
    [118, 225, 13.6],
    [122, 235, 13.7],
    [117, 228, 13.4]
    ])
    a_glicemia = Analisi("glicemia")
    a_colesterolo = Analisi("colesterolo")
    a_emoglobina = Analisi("emoglobina")
    paziente1 = Paziente("Luca","Bianchi","BNCLCU85A01F205Z",39,78.5,analisi_p1)
    paziente2 = Paziente("Giulia","Rossi","RSSGLI97C65L219P",28,62.0,analisi_p2)
    paziente3 = Paziente("Marco","Verdi","VRDMRC73E12M345N",52,84.3,analisi_p3)
    paziente4 = Paziente("Anna", "Moro", "MRTNNA82B41L388P", 43, 64.2, analisi_p4)
    paziente5 = Paziente("Carla", "Neri", "NRECRL59D45M456Z", 66, 70.5, analisi_p5)
    medico1 = Medico("Antonio","Sangue","Ematologia")
    medico2 = Medico("Lucia", "Cuore", "Cardiologia")
    medico3 = Medico("Giovanni", "Sospiro", "Pneumologia")
    print(paziente1.scheda_personale(),"\n")
    print(paziente2.scheda_personale(),"\n")
    print(paziente3.scheda_personale(),"\n")
    print(paziente4.scheda_personale(),"\n")
    print(paziente5.scheda_personale(),"\n")
    print("\n", "\n")
    print(a_glicemia.valuta(paziente1))
    print(a_colesterolo.valuta(paziente3))
    print(a_emoglobina.valuta(paziente5))
    print("\n", "\n")
    print(medico1.visita_paziente(paziente1),"\n")
    print(medico3.visita_paziente(paziente2),"\n")
    print(medico2.visita_paziente(paziente4),"\n")
    print("\n", "\n")
    print(paziente1.statistiche_analisi(),"\n")
    print(paziente2.statistiche_analisi(),"\n")
    print(paziente3.statistiche_analisi(),"\n")
    print(paziente4.statistiche_analisi(),"\n")
    print(paziente5.statistiche_analisi(),"\n")

if __name__ == "__main__":
    main()