import itertools
from graph import Graph


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

    return hamiltonian_cycles


def read_input():
    n = int(input())
    m = {}
    for j in range(n):
        text = input().split(' ')
        m[text[0]] = list(text[1:])
    return m


if __name__ == '__main__':
    test_cases = int(input())

    for i in range(test_cases):
        d = read_input()
        g = Graph(d)
        cycles = brut_algorithm(g)
        print("Test case:", i)
        if len(cycles) > 0:
            print("True", len(cycles))
        else:
            print("False")