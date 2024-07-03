import copy

import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

        self._cromosomi = DAO.getCromosomi()

        self._bestPath = []
        self._bestLun = 0


    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._cromosomi)

        for u in self._grafo.nodes():
            for v in self._grafo.nodes():
                if u != v:
                    peso_arco = DAO.getPeso(u, v)

                    if (DAO.getEdges(u, v)): # controllo prima che esista un arco tra i due nodi (tabella non nulla)
                        self._grafo.add_edge(u, v, weight=peso_arco) # poi lo registro con il relativo peso



    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)

    def getPesoMassimo(self):
        pesoMassimo = 0

        for arco in self._grafo.edges:
            u = arco[0]
            v = arco[1]

            if self._grafo[u][v]['weight'] > pesoMassimo:
                pesoMassimo = self._grafo[u][v]['weight']

        return pesoMassimo

    def getPesoMinimo(self):
        pesoMinimo = -1

        for arco in self._grafo.edges:
            u = arco[0]
            v = arco[1]

            if pesoMinimo == -1:
                pesoMinimo = self._grafo[u][v]['weight']

            elif self._grafo[u][v]['weight'] < pesoMinimo:
                pesoMinimo = self._grafo[u][v]['weight']

        return pesoMinimo


    def contaArchiMaggS(self, soglia):
        archiMaggS = 0

        for arco in self._grafo.edges:
            u = arco[0]
            v = arco[1]
            if self._grafo[u][v]['weight'] > soglia:
                archiMaggS += 1

        return archiMaggS

    def contaArchiMinS(self, soglia):
        archiMinS = 0

        for arco in self._grafo.edges:
            u = arco[0]
            v = arco[1]
            if self._grafo[u][v]['weight'] < soglia:
                archiMinS += 1

        return archiMinS

    def handlePercorso(self, soglia):
        self._bestPath = []
        self._bestLun = 0

        for v0 in self._cromosomi:
            parziale = [v0]
            archiVisitati = []

            self._ricorsione(soglia, parziale, archiVisitati)



        return self._bestPath, self._bestLun


    def _ricorsione(self, soglia, parziale, archiVisitati):

        if self.getScore(parziale) > self._bestLun:
            self._bestLun = self.getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for n in self._grafo.successors(parziale[-1]):
            arcoTemp = (parziale[-1], n)
            arcoTempInv = (n, parziale[-1])
            # essendo un grafo orientato, voglio controllare che l'arco sia attraversato
            # in entrambe le direzioni

            if self._grafo[parziale[-1]][n]['weight'] > soglia:
                if (arcoTemp not in archiVisitati) and (arcoTempInv not in archiVisitati):
                    parziale.append(n)
                    archiVisitati.append(arcoTemp)
                    archiVisitati.append(arcoTempInv)
                    # appendo gli archi in entrambe le direzioni

                    self._ricorsione(soglia, parziale, archiVisitati)
                    parziale.pop()



    def getScore(self, parziale):
        lunghezzaPeso = 0

        if len(parziale) == 1:
            return lunghezzaPeso

        for i in range(len(parziale)-1):
            lunghezzaPeso += self._grafo[parziale[i]][parziale[i+1]]['weight']

        return lunghezzaPeso




