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
