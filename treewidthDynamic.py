import networkx as nx

LEAF_NODE, INTRODUCE_VERTEX_NODE, INTRODUCE_EDGE_NODE = "Leaf node", "Introduce vertex node", "Introduce edge node"
FORGET_NODE, JOIN_NODE, BAG = "Forget node", "Join node", "bag"

def toDecimal(nums, base):
    nums.reverse()
    power = 1
    result = 0
    for i in range(len(nums)):
        result += nums[i] * power
        power = power * base
    return result
def fromDecimal(n, tw, base):
    nums = [0 for x in range(tw)]
    if n == 0:
        return nums
    it = 0
    while n:
        n, r = divmod(n, base)
        nums[it] = r
        it += 1
    nums.reverse()
    return nums
def creteMatrix(G, Tree, labels, root):
    matrix = [[0 for x in range(len(G.edges()))] for y in range(len(G.nodes()))]
    post = postOrderVertex(Tree, labels, root)
    # print(post)
    for v in G.nodes():
        i = 0
        for e in G.edges():
            if v not in e:
                matrix[v][i] = 0
            else:
                idx1 = post.index(e[0])
                idx2 = post.index(e[1])
                if v == e[0] and idx1 > idx2:
                    matrix[v][i] = -1
                elif v == e[1] and idx1 < idx2:
                    matrix[v][i] = -1
                else:
                    matrix[v][i] = 1
            i += 1
    return matrix
def postOrderVertex(Tree, labels, root):
    s1, s2 = [], []
    s1.append(root)
    while s1:
        node = s1.pop()
        if labels[node][0] == FORGET_NODE:
            s2.append(labels[node][1])
        for child in Tree[node]:
            s1.append(child)

    s2.reverse()
    return s2
def postOrderEdges(Tree, labels, root):
    s1, s2 = [], []
    s1.append(root)
    while s1:
        node = s1.pop()
        if labels[node][0] == INTRODUCE_EDGE_NODE:
            s2.append(labels[node][1])
        for child in Tree[node]:
            s1.append(child)

    s2.reverse()
    return s2
def inversion(V1, V2, root):
    result = 0
    post = postOrderVertex(Tree, labels, root)
    for e in G.edges:
        idx1 = post.index(e[0])
        idx2 = post.index(e[1])
        if e[0] in V1 and e[1] in V2 and idx1 > idx2:
            result += 1
    return result
def sign(f, X, root):
    # TODO what is S ??? I claim that S is X
    power = 0
    post = postOrderEdges(Tree, labels, root)
    for e in G.edges():
        if e[0] in X and e[1] in X:
            idx1 = post.index(e[0])
            idx2 = post.index(e[1])
            if idx1 < idx2 and f[e[0]] > f[e[1]]:
                power += 1

    return -1 ** (power % 2)
def functionInverseImage(function, arg, node):
    result = []
    for m in range(len(bags[node])):
        if function[m] == arg:
            result.append(bags[node][m])
    return result


def compute(A, node, i, j, k, matrix, v1, root):
    sDeg = fromDecimal(i, len(bags[node]), 3)
    s1 = fromDecimal(j, len(bags[node]), 2)
    s2 = fromDecimal(k, len(bags[node]), 2)

    if labels[node][0] == LEAF_NODE:
        # print(LEAF_NODE, node)
        A[node][i][j][k] = 1
    elif labels[node][0] == INTRODUCE_VERTEX_NODE:
        # print(INTRODUCE_VERTEX_NODE, node, ", int vertex:", labels[node][1])
        # print("SDEG: ", sDeg, ", S1: ", s1, ", S2: ", s2, sep="")
        v = labels[node][1]
        idx = bags[node].index(v)
        if sDeg[idx] == 0 and s1[idx] == 0 and s2[idx] == 0:
            idx = bags[node].index(v)
            sDeg.pop(idx)
            x = toDecimal(sDeg, 3)
            s1.pop(idx)
            y = toDecimal(s1, 2)
            s2.pop(idx)
            z = toDecimal(s2, 2)
            # print("x:", x, "y:", y, "z:", z)
            A[node][i][j][k] = A[T[node][0]][x][y][z]
        else:
            A[node][i][j][k] = 0
    elif labels[node][0] == INTRODUCE_EDGE_NODE:
        u, v = labels[node][1]
        # print(INTRODUCE_EDGE_NODE, node, ", edge: (", u, ",", v, ")")
        # print("SDEG: ", sDeg, ", S1: ", s1, ", S2: ", s2, sep="")
        idx1 = bags[node].index(u)
        idx2 = bags[node].index(v)

        if sDeg[idx1] >= 1 and sDeg[idx2] >= 1:
            # first sum element
            A[node][i][j][k] = A[T[node][0]][i][j][k]

            # second sum element
            sDeg[idx1] -= 1
            sDeg[idx2] -= 1
            x = toDecimal(sDeg, 3)
            A[node][i][j][k] += A[T[node][0]][x][j][k]

            # third sum element,
            uPrim, vPrim = [], []
            for m in range(len(bags[node])):
                if s1[m] == 1 and bags[node][m] != v1:
                    if bags[node][m] == u or bags[node][m] == v:
                        uPrim.append(bags[node][m])
                if s2[m] == 1 and bags[node][m] != v1:
                    if bags[node][m] == u or bags[node][m] == v:
                        vPrim.append(bags[node][m])

            for uBis in uPrim:
                for vBis in vPrim:
                    # if uBis == vBis:
                    #     continue

                    idx1 = bags[node].index(uBis)
                    idx2 = bags[node].index(vBis)

                    s1Prim = s1
                    s2Prim = s2
                    s1Prim[idx1] = 0
                    s2Prim[idx2] = 0
                    y = toDecimal(s1Prim, 2)
                    z = toDecimal(s2Prim, 2)
                    p = A[T[node][0]][x][y][z]

                    it = 0
                    for e in G.edges():
                        if e[0] == u and e[1] == v or e[0] == v and e[1] == u:
                            break
                        it += 1
                    p = p * matrix[uBis][it] * matrix[vBis][it]

                    list1, list2 = [uBis], [vBis]
                    s1inv = functionInverseImage(s1, 1, node)
                    s2inv = functionInverseImage(s2, 1, node)
                    p = p * (-1) ** (inversion(s1inv, list1, root) + inversion(s2inv, list2, root))

                    A[node][i][j][k] += p
        else:
            A[node][i][j][k] = A[T[node][0]][i][j][k]
    elif labels[node][0] == FORGET_NODE:
        # print(FORGET_NODE, node)
        v = labels[node][1]
        idx = bags[T[node][0]].index(v)
        if v != v1:
            sDeg.insert(idx, 2)
            s1.insert(idx, 1)
            s2.insert(idx, 1)
        else:
            sDeg.insert(idx, 2)
            s1.insert(idx, 0)
            s2.insert(idx, 0)
        x = toDecimal(sDeg, 3)
        y = toDecimal(s1, 2)
        z = toDecimal(s2, 2)
        A[node][i][j][k] = A[T[node][0]][x][y][z]
    elif labels[node][0] == JOIN_NODE:
        # print(JOIN_NODE, node)
        # print(i, j, k)
        sumX = 0
        for s_d in range(i+1):
            for s_1 in range(j+1):
                for s_2 in range(k+1):
                    p = A[T[node][0]][s_d][s_1][s_2]
                    p *= A[T[node][1]][i - s_d][j - s_1][k - s_2]

                    s1Y = fromDecimal(s_1, len(bags[node]), 2)
                    s2Y = fromDecimal(s_2, len(bags[node]), 2)
                    s1Yinv = functionInverseImage(s1Y, 1, node)
                    s2Yinv = functionInverseImage(s2Y, 1, node)

                    s1Z = fromDecimal(j - s_1, len(bags[node]), 2)
                    s2Z = fromDecimal(k - s_2, len(bags[node]), 2)
                    s1Zinv = functionInverseImage(s1Z, 1, node)
                    s2Zinv = functionInverseImage(s2Z, 1, node)

                    p = p * (-1) ** (inversion(s1Yinv, s1Zinv, root) + inversion(s2Yinv, s2Zinv, root))
                    sumX += p
        A[node][i][j][k] = sumX

    return A[node][i][j][k]


def dynamic(root, tw):
    matrix = creteMatrix(G, Tree, labels, root)
    v1 = 2

    A = [[[[0 for k in range(2 ** tw)] for j in range(2 ** tw)] for i in range(3 ** tw)] for x in range(len(Tree))]

    for node in reversed(list(T.keys())):
        # Todo napisac zeby to robic dfsem, najpierw dzieci, wracajac ja
        print("NODE: ", node, ", BAG[NODE]: ", bags[node], sep="")
        for i in range(3 ** len(bags[node])):
            for j in range(2 ** len(bags[node])):
                for k in range(2 ** len(bags[node])):
                    A[node][i][j][k] = compute(A, node, i, j, k, matrix, v1, root)
                    # print("MATRIX A[", node, "][", i, "][", j, "][", k, "]: ", A[node][i][j][k], sep="")
                    # print()
        # print("--------------------------")
        # print("A[", node, "]:", A[node])
        # print("--------------------------", "\n")

    return A[root][0][0][0] / len(G.nodes())


if __name__ == '__main__':
    T = {27: [0],
         0: [1]
        , 1: [2]
        , 2: [3]
        , 3: [4]
        , 4: [5]
        , 5: [6]
        , 6: [7]
        , 7: [8]
        , 8: [9]
        , 9: [10]
        , 10: [11, 19]
        , 11: [12]
        , 12: [13]
        , 13: [14]
        , 14: [15]
        , 15: [16]
        , 16: [17]
        , 17: [18]
        , 18: [19]
        , 19: [20]
        , 20: [21]
        , 21: [22]
        , 22: [23]
        , 23: [24]
        , 24: [25]
        , 25: [26]
        , 26: []
         }

    bags = {27: ([]),
            0: ([0])
        , 1: ([0, 1])
        , 2: ([0, 1])
        , 3: ([1])
        , 4: ([1, 2])
        , 5: ([1, 2])
        , 6: ([3, 1, 2])
        , 7: ([3, 1, 2])
        , 8: ([1, 2, 3, 5])
        , 9: ([1, 2, 3, 5])
        , 10: ([1, 2, 3, 5])
        , 11: ([1, 2, 3, 5])
        , 12: ([2, 3, 5])
        , 13: ([2, 5])
        , 14: ([2, 4, 5])
        , 15: ([2, 4, 5])
        , 16: ([4, 5])
        , 17: ([4, 5])
        , 18: ([5])
        , 19: ([1, 2, 3, 5])
        , 20: ([2, 3, 5])
        , 21: ([3, 5])
        , 22: ([3, 5, 6])
        , 23: ([3, 5, 6])
        , 24: ([5, 6])
        , 25: ([5, 6])
        , 26: ([6])
            }

    labels = {27: (FORGET_NODE, 0),
              0: (FORGET_NODE, 1)
        , 1: (INTRODUCE_EDGE_NODE, (0, 1))
        , 2: (INTRODUCE_VERTEX_NODE, 0)
        , 3: (FORGET_NODE, 2)
        , 4: (INTRODUCE_EDGE_NODE, (1, 2))
        , 5: (FORGET_NODE, 3)
        , 6: (INTRODUCE_EDGE_NODE, (1, 3))
        , 7: (FORGET_NODE, 5)
        , 8: (INTRODUCE_EDGE_NODE, (2, 5))
        , 9: (INTRODUCE_EDGE_NODE, (3, 5))
        , 10: (JOIN_NODE, 0)
        , 11: (INTRODUCE_VERTEX_NODE, 1)
        , 12: (INTRODUCE_VERTEX_NODE, 3)
        , 13: (FORGET_NODE, 4)
        , 14: (INTRODUCE_EDGE_NODE, (2, 4))
        , 15: (INTRODUCE_VERTEX_NODE, 2)
        , 16: (INTRODUCE_EDGE_NODE, (4, 5))
        , 17: (INTRODUCE_VERTEX_NODE, 4)
        , 18: (LEAF_NODE, 5)
        , 19: (INTRODUCE_VERTEX_NODE, 1)
        , 20: (INTRODUCE_VERTEX_NODE, 2)
        , 21: (FORGET_NODE, 6)
        , 22: (INTRODUCE_EDGE_NODE, (3, 6))
        , 23: (INTRODUCE_VERTEX_NODE, 3)
        , 24: (INTRODUCE_EDGE_NODE, (5, 6))
        , 25: (INTRODUCE_VERTEX_NODE, 5)
        , 26: (LEAF_NODE, 6)
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

    print(dynamic(27, 4))
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
    # print("Hamilton cycles number:", dynamic(9, 3))
