import networkx as nx
from copy import deepcopy

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def matchingJoin(u, visited, p1, p2, cycle, one):
    while True:
        if u in visited:
            visited[u] = True
        if one and p2[0][u] == 1:
            u = p2[1][u]
            one = False
        elif not one and p1[0][u] == 1:
            u = p1[1][u]
            one = True
        else:
            break

        if u in visited and visited[u]:
            cycle = True
            break

    return u, cycle, visited

def memoisation(t, hc, T, labels):
    if t in hc.keys():
        return hc[t]

    if labels[t][0] == INTRODUCE_VERTEX_NODE:
        v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
        hc[t] = []
        for pair in childResult:
            pair[0].update({v: 0})
            pair[1].update({v: v})
            hc[t].append(pair)

    elif labels[t][0] == FORGET_NODE:
        v = labels[t][1]
        child = [i for i in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
        hc[t] = []

        for pair in childResult:
            if pair[0][v] == 2:
                del pair[0][v]
                hc[t].append(pair)

    elif labels[t][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
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
                    pair[0].update({u: u_d + 1, v: v_d + 1})
                    u_prim = pair[1][u]
                    v_prim = pair[1][v]
                    pair[1].update({u_prim: v_prim, v_prim: u_prim})
            childResultPrim.append(pair)

        hc[t] = []
        for pair in childResult:
            if pair not in hc[t]:
                hc[t].append(pair)
        for pair in childResultPrim:
            if pair not in hc[t]:
                hc[t].append(pair)

    elif labels[t][0] == JOIN_NODE:
        u = [k for k in T.neighbors(t)][0]
        v = [k for k in T.neighbors(t)][1]

        firstChildResult = memoisation(u, hc, T, labels)
        secondChildResult = memoisation(v, hc, T, labels)

        hc[t] = []
        for p1 in firstChildResult:
            for p2 in secondChildResult:
                if p1 == p2:
                    hc[t].append(p1)
                    continue

                p = ({}, {})
                visited = {}
                cycle = False

                flag = True
                for w in p1[0].keys():
                    deg = p1[0][w] + p2[0][w]
                    if deg > 2:
                        flag = False
                        break

                    p[0].update({w: deg})
                    visited.update({w: False})
                if not flag:
                    continue

                for v in visited.keys():
                    if visited[v]:
                        continue

                    if p1[0][v] == 1 and p2[0][v] == 1:
                        if p1[1][v] != p2[1][v]:
                            u, cycle, visited = matchingJoin(p1[1][v], visited, p1, p2, cycle, True)
                            w, cycle, visited = matchingJoin(p2[1][v], visited, p1, p2, cycle, False)
                            p[1].update({u: w, w: u})
                        else:
                            visited[p1[1][v]] = True
                            p[1].update({v: p1[1][v], p1[1][v]: v})

                    elif p1[0][v] == 1 and p2[0][v] == 0:
                        u, cycle, visited = matchingJoin(p1[1][v], visited, p1, p2, cycle, True)
                        p[1].update({u: v, v: u})

                    elif p1[0][v] == 0 and p2[0][v] == 1:
                        u, cycle, visited = matchingJoin(p2[1][v], visited, p1, p2, cycle, False)
                        p[1].update({u: v, v: u})

                    if cycle:
                        break

                if not cycle and p not in hc[t]:
                    hc[t].append(p)

    elif labels[t][0] == LEAF_NODE:
        hc[t] = [({}, {})]

    # print(t, labels[t])
    return hc[t]


def naiveDynamic(root, treeDecomposition, labels):
    # For every node t store list of pairs (f, M) where f:B_t -> {0, 1, 2} and M is matching on f<-(1)
    # f is represented as dict {key (vertex): value (0, 1, 2)}
    # M is represented as list of tuples of size 2, where tuple is pair of matched vertices
    hc = {}
    result = memoisation(root, hc, treeDecomposition, labels)
    return len(result) > 0
