import itertools


class Graph:
    graph = {}

    def __init__(self, g):
        self.graph = g


def generate_all_permutations(graph):
    vertex_list = []
    for v in graph.graph:
        vertex_list.append(v)

    permutations = list(itertools.permutations(vertex_list))
    return permutations


def check_is_hamiltonian_cycle(graph, p):
    for i in range(0, len(p) - 1):
        current = p[i]
        next_one = p[i + 1]
        if next_one not in graph[current]:
            return False

    return True


def brut_algorithm(graph):
    permutations = generate_all_permutations(graph)
    hamiltonian_cycles = []
    for p in permutations:
        if check_is_hamiltonian_cycle(graph, p):
            hamiltonian_cycles.append(p)

    return hamiltonian_cycles


if __name__ == '__main__':
    # todo read input
    # todo create instance of Graph
    # todo BrutAlgorithm(g)
    # todo print result
    pass
