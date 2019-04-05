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

    for s in sets:
        x = np.setdiff1d(vertex_list, list(s))
        g_prim = graph.subgraph(x)
        h = Graph(g_prim)
        create_adjacent_matrix(h)
        # todo calculate n-th power of matrix
        # todo get corresponding diagonal entry
        pass
    return 0


def read_input():
    n = int(input())
    m = {}
    for j in range(n):
        text = input().split(' ')
        m[text[0]] = list(text[1:])
    return m


if __name__ == '__main__':
    test_cases = int(input())

    for i in range(test_cases):
        d = read_input()
        g = Graph(d)
        cycles = inc_exc_algorithm(g)

        print("Test case:", i)
        if cycles > 0:
            print("True", cycles)
        else:
            print("False")
