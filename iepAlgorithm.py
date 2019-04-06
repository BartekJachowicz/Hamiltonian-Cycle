from itertools import chain, combinations
from graph import Graph
import numpy as np


def power_set(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def create_adjacent_matrix(graph):
    matrix = []
    vertex_list = graph.vertex_list()

    for v in vertex_list:
        a = []
        for u in vertex_list:
            if u in graph.graph[v]:
                a.append(1)
            else:
                a.append(0)
        matrix.append(a)
    return matrix


def inc_exc_algorithm(graph):
    vertex_list = graph.vertex_list()
    sets = power_set(vertex_list)
    result = 0

    for s in sets:
        x = np.setdiff1d(vertex_list, list(s))
        g_prim = graph.subgraph(x)
        h = Graph(g_prim)
        m = create_adjacent_matrix(h)
        if len(m) >= 2:
            matrix = np.linalg.matrix_power(m, len(vertex_list))
            for k in range(len(m)):
                result += (((-1) ** len(s)) * matrix[k][k])
        elif len(m) == 1:
            result += (((-1) ** len(s)) * (m[0][0]**len(vertex_list)))
    return result


