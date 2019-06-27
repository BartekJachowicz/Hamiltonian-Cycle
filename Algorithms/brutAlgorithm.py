import itertools


def generatePermutations(graph):
    vertexList = []
    for v in graph.nodes():
        vertexList.append(v)

    permutations = list(itertools.permutations(vertexList))
    return permutations


def checkIsHamiltonianCycle(graph, p):
    for v in range(0, len(p)):
        current = p[v]
        nextOne = p[(v + 1) % len(p)]
        if (current, nextOne) not in graph.edges():
            return False

    return True


def brutAlgorithm(graph):
    permutations = generatePermutations(graph)
    for p in permutations:
        if checkIsHamiltonianCycle(graph, p):
            return True

    return False
