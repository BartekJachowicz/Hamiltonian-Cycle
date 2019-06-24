from itertools import chain, combinations


class Graph:
    graph = {}

    def __init__(self, g):
        self.graph = g

    def vertex_list(self):
        return list(self.graph.keys())

    def subgraph(self, x):
        g = {}

        for v in self.graph.keys():
            if v in x:
                a = [u for u in self.graph[v] if u in x]
                g[v] = list(a)
        return g

    def power_set(self):
        s = list(self.vertex_list())
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

