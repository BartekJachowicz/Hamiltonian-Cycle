import itertools
import networkx as nx
from copy import deepcopy

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def matchingJoin(u, visited, m1, m2, cycle, one):
    while True:
        visited[u] = True
        if one and (u in m2.keys() and m1[u] != u):
            u = m2[u]
            one = False
        elif not one and (u in m1.keys() and m1[u] != u):
            u = m1[u]
            one = True
        else:
            break

        if visited[u]:
            cycle = True

    return u, cycle, visited
def cuts(U, v):
    out = []
    for i in range(1, len(U) + 1):
        out.extend([(frozenset(V1), frozenset(U.difference(V1))) for V1 in itertools.combinations(U, i) if v in V1])
    return out
def reduce(A, U):
    if not U:
        return A
    v = next(iter(U))
    cutSet = cuts(U, v)

    cutMatrix = {}
    for m in A:
        for cut in cutSet:
            cutMatrix[(frozenset(m), cut)] = int(all((frozenset([k, v]).issubset(cut[0]) or frozenset([k, v]).issubset(cut[1]) for k, v in m.items())))

    result = []
    for i in range(len(A)):
        has_one = False
        p = A[i]
        for cut in cutSet:
            if cutMatrix[(frozenset(p), cut)] == 1:
                has_one = True
                for j in range(i + 1, len(A)):
                    q = A[j]
                    if cutMatrix[(frozenset(q), cut)] == 0:
                        continue
                    for cutPrim in cutSet:
                        cutMatrix[(frozenset(q), cutPrim)] += cutMatrix[(frozenset(p), cutPrim)]
                        cutMatrix[(frozenset(q), cutPrim)] %= 2
                break

        if has_one:
            result.append(A[i])
            if len(result) == 2 ** len(U):
                break

    return result
def functionInverse(f, x):
    result = []
    for t in f:
        if t[1] == x:
            result.append(t[0])
    return result
def fromDecimal(n, length, base):
    nums = [0 for x in range(length)]
    if n == 0:
        return nums
    it = 0
    while n:
        n, r = divmod(n, base)
        nums[it] = r
        it += 1
    nums.reverse()
    return nums

def memoisation(t, s, hc):
    # print(t, s, hc)
    if (t, s) in hc.keys():
        return hc[(t, s)]

    if labels[t][0] == INTRODUCE_VERTEX_NODE:
        v = labels[t][1]
        child = T[t][0]
        childResult = memoisation(child, s.difference([(v, 0)]), hc)

        hc[(t, s)] = []
        for m in childResult:
            match = deepcopy(m)
            # match.update({v: v})
            hc[(t, s)].append(match)

    elif labels[t][0] == FORGET_NODE:
        v = labels[t][1]
        child = T[t][0]
        childResult = memoisation(child, s.union([(v, 2)]), hc)

        hc[(t, s)] = []
        for match in childResult:
            hc[(t, s)].append(match)

    elif labels[t][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[t][1]
        child = T[t][0]

        u_deg, v_deg = 0, 0
        for tup in s:
            if tup[0] == u:
                u_deg = tup[1]
            if tup[0] == v:
                v_deg = tup[1]

        hc[(t, s)] = []
        matchings = []

        if u_deg == 0 or v_deg == 0:
            pass
        elif u_deg == 1 and v_deg == 1:
            recS = s.difference([(v, 1), (u, 1)]).union([(v, 0), (u, 0)])
            mDict = memoisation(child, recS, hc)
            for m in mDict:
                m.update({u: v, v: u})
                if m not in matchings:
                    matchings.append(m)
        elif u_deg == 1 and v_deg == 2:
            recS = s.difference([(v, 2), (u, 1)]).union([(v, 1), (u, 0)])
            mDict = memoisation(child, recS, hc)
            for m in mDict:
                if m == {} or v not in m:
                    continue
                v_prim = m[v]
                m.update({u: v_prim, v_prim: u})
                del m[v]
                if m not in matchings:
                    matchings.append(m)
        elif u_deg == 2 and v_deg == 1:
            recS = s.difference([(v, 1), (u, 2)]).union([(v, 0), (u, 1)])
            mDict = memoisation(child, recS, hc)
            for m in mDict:
                if m == {} or u not in m:
                    continue
                u_prim = m[u]
                m.update({v: u_prim, u_prim: v})
                del m[u]
                if m not in matchings:
                    matchings.append(m)
        else:
            recS = s.difference([(v, 2), (u, 2)]).union([(v, 1), (u, 1)])
            mDict = memoisation(child, recS, hc)
            for m in mDict:
                if m == {} or (u not in m or v not in m):
                    continue
                v_prim = m[v]
                u_prim = m[u]
                if u_prim != v:
                    m.update({u_prim: v_prim, v_prim: u_prim, u: v, v: u})
                if m not in matchings:
                    matchings.append(m)

        childResult = memoisation(child, s, hc)

        for m in childResult:
            hc[(t, s)].append(m)
        for m in matchings:
            if m not in hc[(t, s)]:
                hc[(t, s)].append(m)

    elif labels[t][0] == JOIN_NODE:
        t_1, t_2 = T[t][0], T[t][1]

        hc[(t, s)] = []
        for i in range(3**len(bags[t])):
            l, r = [], []
            nums = fromDecimal(i, len(s), 3)
            j = 0
            for tup in s:
                l.append((tup[0], nums[j]))
                r.append((tup[0], nums[j]))
                j += 1

            firstChildResult = memoisation(t_1, frozenset(l), hc)
            secondChildResult = memoisation(t_2, frozenset(r), hc)

            for m1 in firstChildResult:
                for m2 in secondChildResult:
                    visited = {}
                    m = {}
                    cycle = False

                    inv = functionInverse(s, 1)
                    for v in m1:
                        visited.update({v: False})
                    for v in m2:
                        visited.update({v: False})

                    for v in visited.keys():
                        if visited[v]:
                            continue

                        if (v in m1.keys() and m1[v] != v) and (v in m2.keys() and m2[v] != v):
                            u, cycle, visited = matchingJoin(m1[v], visited, m1, m2, cycle, True)
                            w, cycle, visited = matchingJoin(m2[v], visited, m1, m2, cycle, False)
                            m.update({u: w, w: u})
                        elif (v in m1.keys() and m1[v] != v) and (v not in m2.keys() or m2[v] == v):
                            u, cycle, visited = matchingJoin(m1[v], visited, m1, m2, cycle, True)
                            m.update({u: v, v: u})
                        elif (v not in m1.keys() or m1[v] == v) and (v in m2.keys() and m2[v] != v):
                            u, cycle, visited = matchingJoin(m2[v], visited, m1, m2, cycle, False)
                            m.update({u: v, v: u})

                        if cycle:
                            break

                    if not cycle:
                        hc[(t, s)].append(m)

    elif labels[t][0] == LEAF_NODE:
        hc[(t, s)] = [{}]

    # print("BEFORE REDUCE:", t, labels[t][0], bags[t], hc[(t, s)])

    U = functionInverse(s, 1)
    if len(hc[(t, s)]) > 2**len(U):
        # print(len(hc[(t, s)]), 2**len(U), hc[(t, s)], U, s)
        hc[(t, s)] = reduce(hc[(t, s)], frozenset(U))

    # print("AFTER REDUCE:", t, labels[t][0], bags[t], hc[(t, s)])
    # print("--------------------------------------")

    return hc[(t, s)]


def rankBasedDynamic(root):
    # for every node t store list of pairs (f, M) where f:B_t -> {0, 1, 2} and M is matching on f<-(1)
    # f is represented as dict {key (vertex): value (0, 1, 2)}
    # M is represented as list of tuples of size 2, where tuple is pair of matched vertices
    hc = {}
    s = frozenset([])
    result = memoisation(root, s, hc)
    return len(result) > 0


if __name__ == '__main__':
    # T = {9: [4],
    #      4: [3],
    #      3: [5],
    #      5: [2],
    #      2: [6],
    #      6: [1],
    #      1: [7],
    #      7: [0],
    #      0: [8],
    #      8: []}
    #
    # bags = {9: [],
    #         4: [2],
    #         3: [1, 2],
    #         5: [1, 2],
    #         2: [0, 1, 2],
    #         6: [0, 1, 2],
    #         1: [0, 1],
    #         7: [0, 1],
    #         0: [0],
    #         8: []}
    #
    # labels = {9: (FORGET_NODE, 2),
    #           4: (FORGET_NODE, 1),
    #           3: (INTRODUCE_EDGE_NODE, (1, 2)),
    #           5: (FORGET_NODE, 0),
    #           2: (INTRODUCE_EDGE_NODE, (0, 2)),
    #           6: (INTRODUCE_VERTEX_NODE, 2),
    #           1: (INTRODUCE_EDGE_NODE, (0, 1)),
    #           7: (INTRODUCE_VERTEX_NODE, 1),
    #           0: (INTRODUCE_VERTEX_NODE, 0),
    #           8: (LEAF_NODE, -1)}
    #
    # edges_to_add = []
    # Tree = nx.DiGraph()
    # for key in T.keys():
    #     Tree.add_node(key, bag=bags[key])
    #     for edge in T[key]:
    #         edges_to_add.append((key, edge))
    # Tree.add_edges_from(edges_to_add)
    #
    # G = nx.Graph()
    # G.add_node(0)
    # G.add_node(1)
    # G.add_node(2)
    # G.add_edge(0, 1)
    # G.add_edge(1, 2)
    # G.add_edge(2, 0)
    # print("Hamilton cycles number:", dynamic(9))
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

    print(rankBasedDynamic(27))
