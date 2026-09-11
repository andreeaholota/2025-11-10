import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._storeScelto = None
        self._nodoScelto = None


    def fillDDStore(self):
        for store in self._model.getStores():
            self._view._ddStore.options.append(
                ft.dropdown.Option(key=str(store.store_id), text=str(store.store_name))
            )
        self._view._ddStore.on_change = self.handleStoreChanged

    def handleStoreChanged(self, e):
        self._storeScelto = e.control.value
        self._view.update_page()

    def fillDDNodoScelto(self):
        self._view._ddNode.options.clear()
        for nodo in self._model.getAllNodi():
            self._view._ddNode.options.append(
                ft.dropdown.Option(key=str(nodo.order_id), text= str(nodo.order_id))
            )

        self._view._ddNode.on_change = self.handleNodoChanged
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False

    def handleNodoChanged(self, e):
        self._nodoScelto = e.control.value


    def handleCreaGrafo(self, e):
        k_str = self._view._txtIntK.value

        if self._storeScelto is None or k_str is None or k_str.strip() == "":
            self._view.create_alert("Inserisci un valore per K!")
            return

        try:
            k = int(k_str)
        except ValueError:
            self._view.create_alert("K deve essere un numero!")
            return

        if k <= 0:
            self._view.create_alert("K deve essere positivo!")
            return

        self._model.creaGrafo(self._storeScelto, k)

        top_archi= self._model.archiPesoMaggiore(3)
        self._view.txt_result.controls.append(ft.Text("Top 3 archi:"))
        for n1, n2, dati in top_archi:
            self._view.txt_result.controls.append(ft.Text(f"{n1} - {n2}: peso {dati['weight']}"))

        self.fillDDNodoScelto()
        self._view.update_page()

    def handleCerca(self, e):
        if self._nodoScelto is None:
            self._view.create_alert("Seleziona un nodo!")
            return

        cammino = self._model.getCamminoPiuLungo(str(self._nodoScelto))

        self._view.txt_result.controls.append(ft.Text("Cammino più lungo:"))
        for nodo in cammino:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))
        self._view.txt_result.controls.append(ft.Text(f"Lunghezza: {len(cammino)}"))

        self._view.update_page()

    def handleRicorsione(self, e):
        if self._nodoScelto is None:
            self._view.create_alert("Seleziona un nodo!")
            return
        percorso, peso = self._model.getPercorsoPesoMassimo(str(self._nodoScelto))
        self._view.txt_result.controls.append(ft.Text("Percorso di peso massimo:"))
        for nodo in percorso:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))
        self._view.txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.update_page()