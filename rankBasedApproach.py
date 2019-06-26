import itertools
from copy import deepcopy

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def matchingJoin(u, visited, m1, m2, cycle, one):
    while True:
        if u in visited:
            visited[u] = True
        if one and (u in m2.keys() and m1[u] != u):
            u = m2[u]
            one = False
        elif not one and (u in m1.keys() and m1[u] != u):
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
    for tup in f:
        if tup[1] == x:
            result.append(tup[0])
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
def toDecimal(nums, base):
    power = base ** (len(nums) - 1)
    result = 0
    for tup in nums:
        result += tup[1] * power
        power = power / base
    return result
def generateFunctionsPair(i, s):
    right = []
    left = fromDecimal(i, len(s), 3)

    j = 0
    for tup in s:
        if left[j] > tup[1]:
            return [], [], False
        else:
            right.append(tup[1] - left[j])
        j += 1

    return left, right, True

def memoisation(t, s, hc, T, labels):
    # print(t, s, labels[t])
    if (t, s) in hc.keys():
        # print("BEFORE REDUCE:", "(NODE:)", t, "(LABEL:)", labels[t][0], "(S_DEG:)", s, "(MATCHINGS:)", hc[(t, s)])
        return hc[(t, s)]

    if labels[t][0] == INTRODUCE_VERTEX_NODE:
        v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]
        childResult = []
        # print(child, v, s)
        if (v, 0) in s:
            childResult = memoisation(child, s.difference([(v, 0)]), hc, T, labels)

        hc[(t, s)] = []
        for m in childResult:
            match = deepcopy(m)
            hc[(t, s)].append(match)

    elif labels[t][0] == FORGET_NODE:
        v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]
        childResult = memoisation(child, s.union([(v, 2)]), hc, T, labels)

        hc[(t, s)] = []
        for m in childResult:
            match = deepcopy(m)
            hc[(t, s)].append(match)

    elif labels[t][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[t][1]
        child = [k for k in T.neighbors(t)][0]

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
            mDict = memoisation(child, recS, hc, T, labels)
            # print(mDict)
            for m in mDict:
                match = deepcopy(m)
                match.update({u: v, v: u})
                if match not in matchings:
                    matchings.append(match)
        elif u_deg == 1 and v_deg == 2:
            recS = s.difference([(v, 2), (u, 1)]).union([(v, 1), (u, 0)])
            mDict = memoisation(child, recS, hc, T, labels)
            # print(mDict, hc[(child, recS)])
            for m in mDict:
                match = deepcopy(m)
                if match == {}:
                    if match not in matchings:
                        matchings.append(match)
                    continue
                elif v not in match:
                    continue

                v_prim = match[v]
                match.update({u: v_prim, v_prim: u})
                del match[v]
                if match not in matchings:
                    matchings.append(match)

        elif u_deg == 2 and v_deg == 1:
            recS = s.difference([(v, 1), (u, 2)]).union([(v, 0), (u, 1)])
            mDict = memoisation(child, recS, hc, T, labels)
            # print(mDict, hc[(child, recS)])
            for m in mDict:
                match = deepcopy(m)
                if match == {}:
                    if match not in matchings:
                        matchings.append(match)
                    continue
                elif u not in match:
                    continue

                u_prim = match[u]
                match.update({v: u_prim, u_prim: v})
                del match[u]
                if match not in matchings:
                    matchings.append(match)

        else:
            recS = s.difference([(v, 2), (u, 2)]).union([(v, 1), (u, 1)])
            mDict = memoisation(child, recS, hc, T, labels)
            # print(mDict, hc[(child, recS)])
            for m in mDict:
                match = deepcopy(m)
                if match == {}:
                    if match not in matchings:
                        matchings.append(match)
                    continue
                elif u not in match or v not in match:
                    continue
                v_prim = match[v]
                u_prim = match[u]
                if u_prim != v:
                    match.update({u_prim: v_prim, v_prim: u_prim})
                del match[u]
                del match[v]
                if match not in matchings:
                    matchings.append(match)
        childResult = memoisation(child, s, hc, T, labels)

        for m in childResult:
            match = deepcopy(m)
            hc[(t, s)].append(match)
        for m in matchings:
            if m not in hc[(t, s)]:
                hc[(t, s)].append(m)

    elif labels[t][0] == JOIN_NODE:
        t_1 = [k for k in T.neighbors(t)][0]
        t_2 = [k for k in T.neighbors(t)][1]

        hc[(t, s)] = []
        for i in range(3**len(s)):
            nums_left, nums_right, check = generateFunctionsPair(i, s)

            if not check:
                continue

            j = 0
            l, r = [], []
            for tup in s:
                l.append((tup[0], nums_left[j]))
                r.append((tup[0], nums_right[j]))
                j += 1

            firstChildResult = memoisation(t_1, frozenset(l), hc, T, labels)
            secondChildResult = memoisation(t_2, frozenset(r), hc, T, labels)

            for m1 in firstChildResult:
                for m2 in secondChildResult:
                    visited = {}
                    m = {}
                    cycle = False

                    inv = functionInverse(s, 1)
                    for v in inv:
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

                    if not cycle and m not in hc[(t, s)]:
                        hc[(t, s)].append(m)

    elif labels[t][0] == LEAF_NODE:
        hc[(t, s)] = [{}]

    # print("--------------------------------------")
    # print("BEFORE REDUCE:", "(NODE:)", t, "(LABEL:)", labels[t][0], "(S_DEG:)", s, "(MATCHINGS:)", hc[(t, s)])
    U = functionInverse(s, 1)
    if len(hc[(t, s)]) > 2**len(U):
        print(len(hc[(t, s)]), 2**len(U), hc[(t, s)], U, s)
        hc[(t, s)] = reduce(hc[(t, s)], frozenset(U))
    #
    # print("AFTER REDUCE:", "(NODE:)", t, "(LABEL:)", labels[t][0], "(S_DEG:)", s, "(MATCHINGS:)", hc[(t, s)])
    # print("--------------------------------------")

    return hc[(t, s)]


def rankBasedDynamic(root, treeDecomposition, labels):
    # For every node t store list of pairs (f, M) where f:B_t -> {0, 1, 2} and M is matching on f<-(1)
    # f is represented as dict {key (vertex): value (0, 1, 2)}
    # M is represented as list of tuples of size 2, where tuple is pair of matched vertices
    hc = {}
    s = frozenset([])
    result = memoisation(root, s, hc, treeDecomposition, labels)
    return len(result) > 0
