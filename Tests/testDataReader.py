import networkx as nx

def readData(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    edges = []
    vertices = []

    for line in lines:
        line = line.split(" ")
        if line[0] == "E":
            u, v = int(line[1]), int(line[2])
            edges.append((u, v))

            if u not in vertices:
                vertices.append(u)
            if v not in vertices:
                vertices.append(v)

    return vertices, edges

def createNxGraph(vertices, edges):
    G = nx.Graph()

    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    return G

def readTest(filename):
    vertices, edges = readData(filename)
    G = createNxGraph(vertices, edges)

    return G, edges
