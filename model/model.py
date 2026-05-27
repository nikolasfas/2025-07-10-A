import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapCategories = {}
        self._idMapProducts = {}
        self._products = []
        self._bestPath = []


    def trovaCammino(self, start, end, lenght):

        begginig = self._idMapProducts[int(start)]
        ending = self._idMapProducts[int(end)]
        self._bestPath = []
        self._bestScore = None
        parziale = [begginig]


        self._ricorsione(parziale, ending, lenght, 0)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, end, lenght, punteggio ):
        current = parziale[-1]
        print(parziale)
        if len(parziale) == lenght+1:
            if parziale[-1] == end:
                if self._bestScore is None or punteggio > self._bestScore:

                    self._bestPath = copy.deepcopy(parziale)
                    self._bestScore = punteggio

                return

        for vicino in self._graph.successors(current):
            if vicino not in parziale:

                peso = self._graph[current][vicino]["weight"]

                parziale.append(vicino)
                self._ricorsione(parziale, end, lenght, punteggio + peso)
                parziale.pop()




    def getBestProducts(self):

        weightedProducts = []

        for n in self._graph.nodes:
            somma_entranti = 0

            for u, v, data in self._graph.in_edges(n, data=True):
                somma_entranti += data["weight"]

            somma_uscenti = 0

            for u, v, data in self._graph.out_edges(n, data=True):
                somma_uscenti += data["weight"]

            diff = somma_uscenti - somma_entranti

            weightedProducts.append((n, diff))

        weightedProducts.sort(key = lambda x: x[1], reverse = True)
        top5 = weightedProducts[:5]
        return top5

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategories(self):
        return DAO.getAllCategories(self._idMapCategories)

    def buildGraph(self, category, start, end):
        self._products = DAO.getRightProducts(category)
        for p in self._products:
            self._idMapProducts[p.product_id] = p
        self._graph.add_nodes_from(self._products)
        self._addEdges(category, start, end)


    def _addEdges(self, category, start, end ):

        edgesWeight = DAO.getWeightedEdges(category, start, end)

        for e1 in edgesWeight:
            for e2 in edgesWeight:

                if e1[0] < e2[0]:
                    w1 = int(e1[1])
                    w2 = int(e2[1])
                    sumQ = w1 + w2

                    if w1 > w2:
                        self._graph.add_edge(self._idMapProducts[e1[0]], self._idMapProducts[e2[0]], weight=sumQ)

                    elif w1 == w2:
                        self._graph.add_edge(self._idMapProducts[e1[0]], self._idMapProducts[e2[0]], weight=sumQ)
                        self._graph.add_edge(self._idMapProducts[e2[0]], self._idMapProducts[e1[0]], weight=sumQ)

                    else:
                        self._graph.add_edge(self._idMapProducts[e2[0]], self._idMapProducts[e1[0]], weight=sumQ)



    def getGraphDetails(self):
        return self._graph.nodes, self._graph.edges
