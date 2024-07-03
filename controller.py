import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))

        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi:"))
        self._view.txt_result.controls.append(ft.Text(f"Valore minimo: {self._model.getPesoMinimo()}"))
        self._view.txt_result.controls.append(ft.Text(f"Valore massimo: {self._model.getPesoMassimo()}"))

        self._view.update_page()

    def handle_countedges(self, e):
        soglia = self._view.txt_name.value

        try:
            intSoglia = int(soglia)

        except ValueError:
            self._view.txt_result2.controls.append(ft.Text("Il valore inserito non è un numero"))
            self._view.update_page()
            return

        if intSoglia < self._model.getPesoMinimo() or intSoglia > self._model.getPesoMassimo():
            self._view.create_alert(f"Inserire un numero compreso tra {self._model.getPesoMinimo()} (valore minimo) e {self._model.getPesoMassimo()} (valore massimo)")
            return

        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {self._model.contaArchiMaggS(intSoglia)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {self._model.contaArchiMinS(intSoglia)}"))

        self._view.update_page()

    def handle_search(self, e):
        soglia = self._view.txt_name.value

        try:
            intSoglia = int(soglia)

        except ValueError:
            self._view.txt_result2.controls.append(ft.Text("Il valore inserito non è un numero"))
            self._view.update_page()
            return

        self._view.txt_result3.controls.clear()

        path, lunghezza = self._model.handlePercorso(intSoglia)

        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {lunghezza}"))

        for i in range(len(path) - 1):
            w = self._model._grafo[path[i]][path[i + 1]]["weight"]
            self._view.txt_result3.controls.append(ft.Text(
                f"{path[i]} --> {path[i + 1]}: {w}"))

        self._view.update_page()