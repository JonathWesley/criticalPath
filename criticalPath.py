"""
Trabalho de Grafos
Caminho Critico
Jonath Wesley Herdt
Matheus Emanuel Carraro de Souza
"""

import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, key, weight):
        self.id = key
        self.connectedTo = {}   # sucessores
        self.toConnected = {}   # predecessores
        self.weight = weight    # duracao no node
        self.es = 0             # tempo inicial mais cedo
        self.ef = 0             # tempo final mais cedo
        self.ls = -1            # tempo inicial mais tarde
        self.lf = -1            # tempo final mais tarde
        self.gap = 0            # folga

    def addNeighbor(self, nbr):
        self.connectedTo[nbr] = 1
        nbr.toConnected[self] = 1

    #def __str__(self):
    #    return str(self.id) + ' connected to: ' + str([x.id for x in self.connectedTo])
    
    def setWeight(self, weight):
        self.weight = weight
        
    def setEs(self, es):
        self.es = es
        
    def setEf(self, ef):
        self.ef = ef
        
    def setLs(self, ls):
        self.ls = ls
        
    def setLf(self, lf):
        self.lf = lf
        
    def attGap(self):
        self.gap = self.lf - self.ef

    def getConnections(self):
        return self.connectedTo.keys()
    
    def getPredecessors(self):
        return self.toConnected.keys()

    def getId(self):
        return self.id

    def getWeight(self):
        return self.weight
    
    def getEs(self):
        return self.es
        
    def getEf(self):
        return self.ef
        
    def getLs(self):
        return self.ls
        
    def getLf(self):
        return self.lf
        
    def getGap(self):
        return self.gap

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key, weight):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, weight)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, vert1, vert2, weight = 1):
        if vert1 not in self.vertList:
            self.addVertex(vert1, weight)
        if vert2 not in self.vertList:
            self.addVertex(vert2, weight)
        self.vertList[vert1].addNeighbor(self.vertList[vert2])

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())
    
def earlyTime(vert, time):
    if time >= vert.getEs():
        vert.setEs(time)
        newTime = time + vert.getWeight()
        vert.setEf(newTime)
    for neighbor in vert.getConnections():   
        earlyTime(neighbor, newTime)

def criticalTime(graph):
    maxTime = 0
    for i in range(1, graph.numVertices):
        if graph.getVertex(i).getEf() > maxTime:
            maxTime = graph.getVertex(i).getEf()
    return maxTime
        
def lateTime(vert, time):
    assign = False
    if time <= vert.getLf() or vert.getLf() == -1:
        assign = True
        vert.setLf(time)
        newTime = time - vert.getWeight()
        vert.setLs(newTime)
    for neighbor in vert.getPredecessors():
        if assign :
            lateTime(neighbor, newTime)
        else:
            lateTime(neighbor, vert.getLs())
            
def calculeteGap(graph):
    for i in range(graph.numVertices):
        graph.getVertex(i).attGap()
        
def finalVertices(graph, final):
    for i in range(graph.numVertices-1):
        if not graph.getVertex(i).getConnections():
            graph.addEdge(i, final)

if __name__ == '__main__':
    g = Graph()
    g.addVertex(0, 0) # inicio
        
    lastVertex = 0
    input_file = open("table.txt","r")
    for line in input_file.readlines():
        x = line.split('/')
        g.addVertex(int(x[0]), int(x[1]))
        lastVertex = int(x[0])
        y = x[2].split(',')
        if y[0] == '\n':
            y = '0'
        else:
            y[-1] = y[-1].replace('\n','')
        for i in y:
            g.addEdge(int(i), int(x[0]))
        
    g.addVertex(lastVertex+1, 0) # fim
    
    finalVertices(g, lastVertex+1)
    
    #for i in range(g.numVertices):
    #    print(g.getVertex(i))
    
    earlyTime(g.getVertex(0), 0)
    
    cTime = criticalTime(g)
    
    lateTime(g.getVertex(lastVertex+1), cTime)
    
    calculeteGap(g)
    
    #for i in range(1, g.numVertices - 1):
    #    print(str(i) + ": " + str(g.getVertex(i).getEs()) + "-" + str(g.getVertex(i).getEf()) + " / " + str(g.getVertex(i).getLs()) + "-" + str(g.getVertex(i).getLf()) + " / " + str(g.getVertex(i).getGap()))
        
    G = nx.DiGraph()
    
    for i in range(g.numVertices):
        if i == 0:
            string = "Início"
        elif i == lastVertex+1:
            string = "Fim"
        else:
            string = "ID:"+str(g.getVertex(i).getId())+"\nFolga:"+str(g.getVertex(i).getGap())
        G.add_node(string)
    
    for i in range(g.numVertices):
        for j in g.getVertex(i).getConnections():
            if i == 0:
                stringI = "Início"
            else:
                stringI = "ID:"+str(g.getVertex(i).getId())+"\nFolga:"+str(g.getVertex(i).getGap())
            if j.getId() == lastVertex+1:
                stringJ = "Fim"
            else:
                stringJ = "ID:"+str(g.getVertex(j.getId()).getId())+"\nFolga:"+str(g.getVertex(j.getId()).getGap())
            G.add_edge(stringI, stringJ)
    
    color_map = []
    for i in range(g.numVertices):
        if i == 0 or i == lastVertex+1:
            color_map.append('green')
        elif g.getVertex(i).getGap() == 0:
            color_map.append('red')
        else:
            color_map.append('blue')
            
    nx.draw_networkx(G, arrows=True, with_labels=True, node_size=2500, node_color=color_map)