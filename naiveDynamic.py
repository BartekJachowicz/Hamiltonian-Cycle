import networkx as nx
from copy import deepcopy

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def matchingJoin(u, visited, p1, p2, cycle, one):
    while True:
        visited[u] = True
        if one and p2[0][u] == 1:
            u = p2[1][u]
            one = False
        elif not one and p1[0][u] == 1:
            u = p1[1][u]
            one = True
        else:
            break

        if visited[u]:
            cycle = True

    return u, cycle, visited

def memoisation(t, hc):
    if t in hc.keys():
        return hc[t]

    if labels[t][0] == INTRODUCE_VERTEX_NODE:
        v = labels[t][1]
        child = T[t][0]

        childResult = memoisation(child, hc)
        hc[t] = []
        for pair in childResult:
            pair[0].update({v: 0})
            pair[1].update({v: v})
            hc[t].append(pair)

    elif labels[t][0] == FORGET_NODE:
        v = labels[t][1]
        child = T[t][0]

        childResult = memoisation(child, hc)
        hc[t] = []

        for pair in childResult:
            if pair[0][v] == 2:
                del pair[0][v]
                hc[t].append(pair)

    elif labels[t][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[t][1]
        child = T[t][0]

        childResult = memoisation(child, hc)
        childResultPrim = []
        for p in childResult:
            pair = deepcopy(p)
            u_d = pair[0][u]
            v_d = pair[0][v]

            if u_d == 2 or v_d == 2:
                continue
            elif u_d == 0 and v_d == 0:
                pair[0].update({u: u_d + 1, v: v_d + 1})
                pair[1].update({u: v, v: u})
            elif u_d == 1 and v_d == 0:
                pair[0].update({u: u_d + 1, v: v_d + 1})
                u_prim = pair[1][u]
                del pair[1][u]
                pair[1].update({v: u_prim, u_prim: v})
            elif u_d == 0 and v_d == 1:
                pair[0].update({u: u_d + 1, v: v_d + 1})
                v_prim = pair[1][v]
                del pair[1][v]
                pair[1].update({u: v_prim, v_prim: u})
            elif u_d == 1 and v_d == 1:
                if pair[1][u] == v:
                    pair[0].update({u: u_d + 1, v: v_d + 1})
                    del pair[1][u]
                    del pair[1][v]
                else:
                    u_prim = pair[1][u]
                    v_prim = pair[1][v]
                    pair[1].update({u_prim: v_prim, v_prim: u_prim, u: v, v: u})
            childResultPrim.append(pair)

        hc[t] = []
        for pair in childResult:
            if pair not in hc[t]:
                hc[t].append(pair)
        for pair in childResultPrim:
            if pair not in hc[t]:
                hc[t].append(pair)

    elif labels[t][0] == JOIN_NODE:
        u, v = T[t][0], T[t][1]

        firstChildResult = memoisation(u, hc)
        secondChildResult = memoisation(v, hc)

        hc[t] = []
        for p1 in firstChildResult:
            for p2 in secondChildResult:
                p = ({}, {})
                visited = {}
                cycle = False

                for v in p1[0].keys():
                    deg = p1[0][v] + p2[0][v]
                    if deg > 2:
                        continue

                    p[0].update({v: deg})
                    visited.update({v: False})

                for v in visited.keys():
                    if visited[v]:
                        continue

                    if p1[0][v] == 1 and p2[0][v] == 1:
                        u, cycle, visited = matchingJoin(p1[1][v], visited, p1, p2, cycle, True)
                        w, cycle, visited = matchingJoin(p2[1][v], visited, p1, p2, cycle, False)
                        p[1].update({u: w, w: u})
                    elif p1[0][v] == 1 and p2[0][v] == 0:
                        u, cycle, visited = matchingJoin(p1[1][v], visited, p1, p2, cycle, True)
                        p[1].update({u: v, v: u})
                    elif p1[0][v] == 0 and p2[0][v] == 1:
                        u, cycle, visited = matchingJoin(p2[1][v], visited, p1, p2, cycle, False)
                        p[1].update({u: v, v: u})

                    if cycle:
                        break

                if not cycle:
                    hc[t].append(p)

    elif labels[t][0] == LEAF_NODE:
        hc[t] = [({}, {})]

    print(t, labels[t][0], hc[t])
    return hc[t]


def naiveDynamic(root):
    # for every node t store list of pairs (f, M) where f:B_t -> {0, 1, 2} and M is matching on f<-(1)
    # f is represented as dict {key (vertex): value (0, 1, 2)}
    # M is represented as list of tuples of size 2, where tuple is pair of matched vertices
    hc = {}
    result = memoisation(root, hc)
    return len(result) > 0


if __name__ == '__main__':
    T = {27: [0],
         0: [1],
         1: [2],
         2: [3],
         3: [4],
         4: [5],
         5: [6],
         6: [7],
         7: [8],
         8: [9],
         9: [10],
         10: [11, 19],
         11: [12],
         12: [13],
         13: [14],
         14: [15],
         15: [16],
         16: [17],
         17: [18],
         18: [28],
         28: [],
         19: [20],
         20: [21],
         21: [22],
         22: [23],
         23: [24],
         24: [25],
         25: [26],
         26: [29],
         29: []
         }

    bags = {27: frozenset([]),
            0: frozenset([0]),
            1: frozenset([0, 1]),
            2: frozenset([0, 1]),
            3: frozenset([1]),
            4: frozenset([1, 2]),
            5: frozenset([1, 2]),
            6: frozenset([3, 1, 2]),
            7: frozenset([3, 1, 2]),
            8: frozenset([1, 2, 3, 5]),
            9: frozenset([1, 2, 3, 5]),
            10: frozenset([1, 2, 3, 5]),
            11: frozenset([1, 2, 3, 5]),
            12: frozenset([2, 3, 5]),
            13: frozenset([2, 5]),
            14: frozenset([2, 4, 5]),
            15: frozenset([2, 4, 5]),
            16: frozenset([4, 5]),
            17: frozenset([4, 5]),
            18: frozenset([5]),
            28: frozenset([]),
            19: frozenset([1, 2, 3, 5]),
            20: frozenset([2, 3, 5]),
            21: frozenset([3, 5]),
            22: frozenset([3, 5, 6]),
            23: frozenset([3, 5, 6]),
            24: frozenset([5, 6]),
            25: frozenset([5, 6]),
            26: frozenset([6]),
            29: frozenset([])
            }

    labels = {27: (FORGET_NODE, 0),
              0: (FORGET_NODE, 1),
              1: (INTRODUCE_EDGE_NODE, (0, 1)),
              2: (INTRODUCE_VERTEX_NODE, 0),
              3: (FORGET_NODE, 2),
              4: (INTRODUCE_EDGE_NODE, (1, 2)),
              5: (FORGET_NODE, 3),
              6: (INTRODUCE_EDGE_NODE, (1, 3)),
              7: (FORGET_NODE, 5),
              8: (INTRODUCE_EDGE_NODE, (2, 5)),
              9: (INTRODUCE_EDGE_NODE, (3, 5)),
              10: (JOIN_NODE, 0),
              11: (INTRODUCE_VERTEX_NODE, 1),
              12: (INTRODUCE_VERTEX_NODE, 3),
              13: (FORGET_NODE, 4),
              14: (INTRODUCE_EDGE_NODE, (2, 4)),
              15: (INTRODUCE_VERTEX_NODE, 2),
              16: (INTRODUCE_EDGE_NODE, (4, 5)),
              17: (INTRODUCE_VERTEX_NODE, 4),
              18: (INTRODUCE_VERTEX_NODE, 5),
              28: (LEAF_NODE, -1),
              19: (INTRODUCE_VERTEX_NODE, 1),
              20: (INTRODUCE_VERTEX_NODE, 2),
              21: (FORGET_NODE, 6),
              22: (INTRODUCE_EDGE_NODE, (3, 6)),
              23: (INTRODUCE_VERTEX_NODE, 3),
              24: (INTRODUCE_EDGE_NODE, (5, 6)),
              25: (INTRODUCE_VERTEX_NODE, 5),
              26: (INTRODUCE_VERTEX_NODE, 6),
              29: (LEAF_NODE, -1)
              }

    G = nx.Graph()
    for i in range(7):
        G.add_node(i)
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (3, 6), (4, 5), (5, 6)])

    edges_to_add = []
    Tree = nx.DiGraph()
    for x in T.keys():
        Tree.add_node(x, bag=bags[x])
        # print(x, Tree.node[x][bag])
        for y in T[x]:
            edges_to_add.append((x, y))
    Tree.add_edges_from(edges_to_add)

    print(naiveDynamic(27))
