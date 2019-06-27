from itertools import chain, combinations

def calculateMasks(sets):
    maskSet = {}
    for s in sets:
        mask = 0
        for i in s:
            mask += (2**i)
        maskSet[s] = mask
    return maskSet


def checkBit(mask, bit):
    return mask & (2**bit)


def dynamicAlgorithm(graph):
    vertexList = list(graph.nodes())
    sets = list(chain.from_iterable(combinations(vertexList, r) for r in range(len(vertexList) + 1)))
    maskSet = calculateMasks(sets)

    x = vertexList[0]

    dp = [[False for i in range(len(vertexList))] for j in range(len(sets))]

    for s in sets:
        if len(s) == 2 and x in s:
            if (x, s[1]) in graph.edges() or (s[1], x) in graph.edges():
                dp[maskSet[s]][s[1]] = True

    for s in sets:
        for v in s:
            for u in s:
                if u == v or ((u, v) not in graph.edges() and (v, u) not in graph.edges()):
                    continue
                m = maskSet[s] - 2**v
                if dp[m][u]:
                    dp[maskSet[s]][v] = True
                    break

    for v in vertexList:
        if dp[2**len(vertexList) - 1][v] and ((v, x) in graph.edges() or (x, v) in graph.edges()):
            return True

    return False
