from graph import Graph
from brutAlgorithm import brut_algorithm
from iepAlgorithm import inc_exc_algorithm
from dynamicAlgorithm import dynamic_algorithm
from random import randint


def test_algorithm(g):
    brut = brut_algorithm(g)
    iep = inc_exc_algorithm(g)
    dynamic = dynamic_algorithm(g)

    print("BRUT:", brut)
    print("IEP:", iep)
    print("DYNAMIC:", dynamic)


def generate_test():
    vertex_number = randint(2, 10)
    d = {}
    for v in range(vertex_number):
        s = []
        n = randint(0, vertex_number - 1)
        for j in range(n):
            u = v
            while u == v or u in s:
                u = randint(0, vertex_number - 1)
            s.append(u)
        d[v] = s
    return Graph(d)


if __name__ == '__main__':
    tests_number = randint(1, 10)

    for i in range(tests_number):
        print("Test number:", i)
        g = generate_test()
        test_algorithm(g)
        print()

