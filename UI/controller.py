import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._category = self._view._ddcategory.value
        first, last = self._model.getDateRange()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Date selezionate: \nStart date: {first}\nEnd date: {last}")
        )
        self._model.buildGraph(self._category, first, last)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato: \nNumero di nodi: {len(nodes)}\nNumero di archi: {len(edges)}")
        )
        self._view.update_page()

        nodes, edges = self._model.getGraphDetails()

        for n in nodes:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(
                    data=n,
                    key=n.product_id,
                    text=n.product_name,
                )
            )
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(
                    data=n,
                    key=n.product_id,
                    text=n.product_name,
                )
            )
        self._view.update_page()


    def handleBestProdotti(self, e):
        top5 = self._model.getBestProducts()
        self._view.txt_result.controls.append(
            ft.Text("I cinque prodotti più venduti sono: ")
        )

        for p in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} with score {p[1]}")
            )
        self._view.update_page()



    def handleCercaCammino(self, e):
        start = self._view._ddProdStart.value
        end = self._view._ddProdEnd.value
        lenght = self._view._txtInLun.value

        if start is None or end is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare prodotto di partenza e arrivo.", color="red")
            )
            self._view.update_page()
            return

        try:
            intLenght = int(lenght)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Per favore immettere un valore intero positivo!", color="red")
            )
            self._view.update_page()
            return

        bestPath, bestScore = self._model.trovaCammino(start, end, intLenght)

        self._view.txt_result.controls.clear()

        if bestPath is None or len(bestPath) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato.", color="red")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino ottimo è lungo {len(bestPath)} e la somma dei pesi è {bestScore}")
        )

        for p in bestPath:
            self._view.txt_result.controls.append(
                ft.Text(str(p))
            )

        self._view.update_page()




    def _fillDDCategories(self):
        categoriesMap = self._model.getAllCategories()

        for category_id, category_name in categoriesMap.items():
            self._view._ddcategory.options.append(
                ft.dropdown.Option(
                    data=category_id,
                    key= str(category_id),
                    text = category_name,
                )
            )
        self._view.update_page()



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
