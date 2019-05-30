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


NODE_TYPE = {'iv': "INTRODUCE_VERTEX_NODE", 'f': "FORGET_NODE", 'j': "JOIN_NODE",
             'l': "LEAF_NODE", 'ie': "INTRODUCE_EDGE_NODE", 'b': "BLANK"}


class NODE:
    type = ''
    label = []
    neighbour = []

    def __init__(self, t, l, n):
        self.type = t
        self.label = l
        self.neighbour = n


class HARDCODE_NTD:
    G = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4, 5], 3: [1, 4], 4: [2, 3, 5], 5: [2, 4]}

    u0 = NODE(NODE_TYPE['b'], [0, 1, 2], [])
    u1 = NODE(NODE_TYPE['b'], [1, 2, 3], [])
    u2 = NODE(NODE_TYPE['b'], [2, 3, 4], [])
    u3 = NODE(NODE_TYPE['b'], [3, 4, 5], [])
    u0.neighbour.append(u1)
    u1.neighbour.append(u2)
    u2.neighbour.append(u3)

    TD = {u0, u1, u2, u3}

    n0 = NODE(NODE_TYPE['i'], [], [])
    n1 = NODE(NODE_TYPE['i'], [1], [])
    n2 = NODE(NODE_TYPE['i'], [1, 2], [])
    n3 = NODE(NODE_TYPE['j'], [1, 2, 3], [])
    n4 = NODE(NODE_TYPE['f'], [1, 2, 3], [])
    n5 = NODE(NODE_TYPE['i'], [1, 2], [])
    n6 = NODE(NODE_TYPE['f'], [0, 1, 2], [])
    n7 = NODE(NODE_TYPE['f'], [0, 1], [])
    n8 = NODE(NODE_TYPE['l'], [0], [])
    n9 = NODE(NODE_TYPE['f'], [1, 2, 3], [])
    n10 = NODE(NODE_TYPE['i'], [2, 3], [])
    n11 = NODE(NODE_TYPE['f'], [2, 3, 4], [])
    n12 = NODE(NODE_TYPE['i'], [2, 4], [])
    n13 = NODE(NODE_TYPE['f'], [2, 4, 5], [])
    n14 = NODE(NODE_TYPE['f'], [4, 5], [])
    n15 = NODE(NODE_TYPE['l'], [5], [])

    n0.neighbour.append(n1)
    n1.neighbour.append(n2)
    n2.neighbour.append(n3)
    n3.neighbour.append(n4)
    n3.neighbour.append(n9)
    n4.neighbour.append(n5)
    n5.neighbour.append(n6)
    n6.neighbour.append(n7)
    n7.neighbour.append(n8)
    n9.neighbour.append(n10)
    n10.neighbour.append(n11)
    n11.neighbour.append(n12)
    n12.neighbour.append(n13)
    n13.neighbour.append(n14)
    n14.neighbour.append(n15)

    NTD = {n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, 15}

