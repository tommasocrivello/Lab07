import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    # TODO
    def popola_dropdowns(self):
        """ Legge i dati dal Model e riempie le tendine dell'interfaccia Flet """
        # 1. Popola Dropdown Biblioteche
        self._view.dd_biblioteca.options.append(ft.dropdown.Option(key="Nessun filtro", text="Nessun filtro"))

        biblioteche = self._model.get_biblioteche()
        if biblioteche is not None:
            for b in biblioteche:
                # La key è l'ID numerico (convertito in stringa per Flet), il text è il nome leggibile
                self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=str(b.id), text=b.nome))

        # 2. Popola Dropdown Generi
        self._view.dd_genere.options.append(ft.dropdown.Option(key="Nessun filtro", text="Nessun filtro"))

        generi = self._model.get_generi()
        if generi is not None:
            for g in generi:
                # Per i generi, key e text sono identici
                self._view.dd_genere.options.append(ft.dropdown.Option(key=g, text=g))

        self._view.update()

    # CALLBACKS DROPDOWN
    # TODO
    def seleziona_biblioteca(self, e):
        self.biblioteca_selezionata = self._view.dd_biblioteca.value

    def seleziona_genere(self, e):
        self.genere_selezionato = self._view.dd_genere.value

    # AZIONE: MOSTRA LIBRI
    # TODO
    def mostra_libri(self, e):
        # 1. Leggiamo i valori attualmente selezionati
        scelta_bibl = self._view.dd_biblioteca.value
        scelta_genere = self._view.dd_genere.value

        # 2. Validazione base: se non ha toccato proprio i menu, Flet restituisce None
        # Traduciamo i testi della UI nei tipi di dato puri che servono al database
        id_bibl_pulito = None if scelta_bibl == "Nessun filtro" or scelta_bibl is None else int(scelta_bibl)
        genere_pulito = None if scelta_genere == "Nessun filtro" or scelta_genere is None else scelta_genere

        # 3. Interroghiamo il Model "passacarte"
        libri = self._model.get_libri_filtrati(genere_pulito, id_bibl_pulito)

        # 4. Aggiorniamo la View
        self._view.lista_libri.controls.clear()

        if libri is None:
            self._view.show_alert("❌ Errore di connessione al database.")
        elif len(libri) == 0:
            self._view.show_alert("❌ Nessun libro trovato con questi filtri.")
        else:
            for libro in libri:
                self._view.lista_libri.controls.append(ft.Text(str(libro)))

        self._view.update()