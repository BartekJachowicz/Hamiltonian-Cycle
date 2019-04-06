import itertools


def generate_all_permutations(graph):
    vertex_list = []
    for v in graph.graph:
        vertex_list.append(v)

    permutations = list(itertools.permutations(vertex_list))
    return permutations


def check_is_hamiltonian_cycle(graph, p):
    for v in range(0, len(p)):
        current = p[v]
        next_one = p[(v + 1) % len(p)]
        if next_one not in graph.graph[current]:
            return False

    return True


def brut_algorithm(graph):
    permutations = generate_all_permutations(graph)
    hamiltonian_cycles = []
    for p in permutations:
        if check_is_hamiltonian_cycle(graph, p):
            hamiltonian_cycles.append(p)

    return len(hamiltonian_cycles)
