import itertools
from copy import deepcopy

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def matchingJoin(u, visited, key1, m1, key2, m2, cycle, one):
    while True:
        if u in visited:
            visited[u] = True
        if one and key2[u] == 1:
            u = m2[u]
            one = False
        elif not one and key1[u] == 1:
            u = m1[u]
            one = True
        else:
            break

        if u in visited and visited[u]:
            cycle = True
            break

    return u, cycle, visited
def cuts(U, v):
    out = []
    for i in range(1, len(U) + 1):
        out.extend([(frozenset(V1), frozenset(U.difference(V1))) for V1 in itertools.combinations(U, i) if v in V1])
    return out

def reduce(A, U):
    if len(A) < len(U):
        return A

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
    for v in f:
        if f[v] == x:
            result.append(v)
    return result


def memoisation(t, hc, T, labels):
    # print(t, labels[t])
    if t in hc.keys():
        return hc[t]

    if labels[t][0] == INTRODUCE_VERTEX_NODE:
        v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
        hc[t] = []
        for tup in childResult:
            k = deepcopy(tup[0])
            val = deepcopy(tup[1])
            k.update({v: 0})
            # for match in val:
            #     match.update({v: v})
            hc[t].append((k, val))

    elif labels[t][0] == FORGET_NODE:
        v = labels[t][1]
        child = [i for i in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
        hc[t] = []

        for tup in childResult:
            if tup[0][v] == 2:
                k = deepcopy(tup[0])
                val = deepcopy(tup[1])
                del k[v]
                hc[t].append((k, val))

    elif labels[t][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]

        childResult = memoisation(child, hc, T, labels)
        childResultPrim = []
        for tup in childResult:
            k = deepcopy(tup[0])
            val = deepcopy(tup[1])
            u_d = k[u]
            v_d = k[v]

            if u_d == 2 or v_d == 2:
                continue
            elif u_d == 0 and v_d == 0:
                k.update({u: u_d + 1, v: v_d + 1})
                for match in val:
                    match.update({u: v, v: u})
            elif u_d == 1 and v_d == 0:
                k.update({u: u_d + 1, v: v_d + 1})
                for match in val:
                    u_prim = match[u]
                    del match[u]
                    match.update({v: u_prim, u_prim: v})
            elif u_d == 0 and v_d == 1:
                k.update({u: u_d + 1, v: v_d + 1})
                for match in val:
                    v_prim = match[v]
                    del match[v]
                    match.update({u: v_prim, v_prim: u})
            elif u_d == 1 and v_d == 1:
                for match in val:
                    if match[u] == v:
                        k.update({u: u_d + 1, v: v_d + 1})
                        del match[u]
                        del match[v]
                    else:
                        k.update({u: u_d + 1, v: v_d + 1})
                        u_prim = match[u]
                        v_prim = match[v]
                        match.update({u_prim: v_prim, v_prim: u_prim})
            childResultPrim.append((k, val))

        hc[t] = []
        for tup in childResult:
            if tup not in hc[t]:
                k = deepcopy(tup[0])
                val = deepcopy(tup[1])
                hc[t].append((k, val))
        for tup in childResultPrim:
            if tup not in hc[t]:
                hc[t].append(tup)

    elif labels[t][0] == JOIN_NODE:
        u = [k for k in T.neighbors(t)][0]
        v = [k for k in T.neighbors(t)][1]

        firstChildResult = memoisation(u, hc, T, labels)
        secondChildResult = memoisation(v, hc, T, labels)

        hc[t] = []
        for tup1 in firstChildResult:
            for tup2 in secondChildResult:
                if tup1 == tup2:
                    hc[t].append(tup1)
                    continue

                key1 = deepcopy(tup1[0])
                value1 = deepcopy(tup1[1])
                key2 = deepcopy(tup2[0])
                value2 = deepcopy(tup2[1])

                flag = True
                k, visited = {}, {}
                for w in key1.keys():
                    deg = key1[w] + key2[w]
                    if deg > 2:
                        flag = False
                        break

                    k.update({w: deg})
                    visited.update({w: False})
                if not flag:
                    continue

                val = []
                for m1 in value1:
                    for m2 in value2:
                        match = {}
                        cycle = False

                        for v in visited.keys():
                            if visited[v]:
                                continue

                            if key1[v] == 1 and key2[v] == 1:
                                if m1[v] != m2[v]:
                                    u, cycle, visited = matchingJoin(m1[v], visited, key1, m1, key2, m2, cycle, True)
                                    w, cycle, visited = matchingJoin(m2[v], visited, key1, m1, key2, m2, cycle, False)
                                    match.update({u: w, w: u})
                                else:
                                    visited[m1[v]] = True
                                    match.update({v: m1[v], m1[v]: v})

                            elif key1[v] == 1 and key2[v] == 0:
                                u, cycle, visited = matchingJoin(m1[v], visited, key1, m1, key2, m2, cycle, True)
                                match.update({u: v, v: u})

                            elif key1[v] == 0 and key2[v] == 1:
                                u, cycle, visited = matchingJoin(m2[v], visited, key1, m1, key2, m2, cycle, False)
                                match.update({u: v, v: u})

                            if cycle:
                                break

                        if not cycle and match not in val:
                            val.append(match)

                if (k, val) not in hc[t]:
                    hc[t].append((k, val))

    elif labels[t][0] == LEAF_NODE:
        hc[t] = [({}, [{}])]

    hcReduced = []
    for tup in hc[t]:
        U = functionInverse(tup[0], 1)
        newMatchSet = reduce(tup[1], frozenset(U))
        hcReduced.append((tup[0], newMatchSet))

    hc[t] = hcReduced

    # print("Return:", t, labels[t])
    return hc[t]


def rankBasedDynamicVol2(root, treeDecomposition, labels):
    # For every node t store list of tuples: dict f:B_t -> {0, 1, 2} and array of M's, where M are matchings on f<-(1)
    # f is represented as dict {key (vertex): value (0, 1, 2)}
    # Matching is represented as list of tuples of size 2, where tuple is pair of matched vertices
    hc = {}
    result = memoisation(root, hc, treeDecomposition, labels)
    return len(result) > 0
