import copy

import networkx as nx

from database.DAO import DAO
from datetime import date, datetime, timedelta

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

    def creaGrafo(self, stores_id, K):
        self._graph.clear()
        self._idMap.clear()

        vertici = DAO.getAllOrder(stores_id)
        for v in vertici:
            self._idMap[v.order_id] = v
        self._graph.add_nodes_from(vertici)

        for v1, v2, wight in DAO.getOrdersByDate(stores_id, K):
            self._graph.add_edge(self._idMap[v1], self._idMap[v2], weight=wight)


    def getNumVertici(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getAllNodi(self):
        return list(self._graph.nodes())

    def archiPesoMaggiore(self, n):
        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda edge: edge[2]["weight"], reverse=True)
        return edges[:n]

    def getCamminoPiuLungo(self, nodoStr):
        start = self._idMap[int(nodoStr)]
        self._bestPath = [start]
        self._dfs(start, [start])
        return self._bestPath

    def _dfs(self, corrente, parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        for v in self._graph.neighbors(corrente):  # successors(corrente) se orientato
            if v not in parziale:
                parziale.append(v)
                self._dfs(v, parziale)
                parziale.pop()


    def getPercorsoPesoMassimo(self, nodo_iniziale_str):
        start = self._idMap[int(nodo_iniziale_str)]
        self._bestPath = [start]
        self._bestPeso = 0
        self._ricorsione(start, [start], None, 0)
        return self._bestPath, self._bestPeso

    def _ricorsione(self, corrente, parziale, ultimo_peso, peso_acc):
        if peso_acc > self._bestPeso:
            self._bestPeso = peso_acc
            self._bestPath = copy.deepcopy(parziale)

        for vicino in self._graph.successors(corrente):
            if vicino not in parziale:
                peso_arco = self._graph[corrente][vicino]["weight"]
                if ultimo_peso is None or peso_arco < ultimo_peso:
                    parziale.append(vicino)
                    self._ricorsione(vicino, parziale, peso_arco, peso_acc + peso_arco)
                    parziale.pop()

















