import numpy as np
import networkx as nx
from itertools import chain, combinations


def createAdjacentMatrix(graph):
    matrix = []
    vertexList = graph.nodes()

    for v in vertexList:
        a = []
        for u in vertexList:
            if (v, u) in graph.edges():
                a.append(1)
            else:
                a.append(0)
        matrix.append(a)
    return matrix

def subgraph(graph, x):
    g = nx.Graph()

    g.add_nodes_from(x)

    for edge in graph.edges():
        if edge[0] in x and edge[1] in x:
            g.add_edge(edge[0], edge[1])
    return g


def incExcAlgorithm(graph):
    vertexList = graph.nodes()
    vL = list(vertexList)
    sets = list(chain.from_iterable(combinations(vL, r) for r in range(len(vL) + 1)))

    result = 0

    for s in sets:
        x = np.setdiff1d(vertexList, list(s))
        h = subgraph(graph, x)
        m = createAdjacentMatrix(h)
        if len(m) >= 2:
            matrix = np.linalg.matrix_power(m, len(vertexList))
            for k in range(len(m)):
                result += (((-1) ** len(s)) * matrix[k][k])
        elif len(m) == 1:
            result += (((-1) ** len(s)) * (m[0][0]**len(vertexList)))
    return result
