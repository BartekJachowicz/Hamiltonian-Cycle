from graph import Graph
from brutAlgorithm import brut_algorithm
from iepAlgorithm import inc_exc_algorithm
from dynamicAlgorithm import dynamic_algorithm
from random import randint


def test_algorithm(g):
    brut = brut_algorithm(g)
    iep = inc_exc_algorithm(g)
    dynamic = dynamic_algorithm(g)

    print("Test case:", i)
    print_algorithm_result(brut, "BRUT")
    print_algorithm_result(iep, "IEP")
    print_algorithm_result(dynamic, "DYNAMIC")


def print_algorithm_result(result, algorithm):
    if result > 0:
        print(algorithm, ":", "True", result)
    else:
        print(algorithm, ":", "False")


def generate_test():
    vertex_number = randint(2, 10)
    d = {}
    for v in range(vertex_number):
        s = []
        n = randint(0, vertex_number-1)
        for j in range(n):
            u = v
            while u == v or u in s:
                u = randint(0, vertex_number)
            s.append(u)
        d[v] = s
    print(d)
    return Graph(d)


if __name__ == '__main__':
    tests_number = randint(1, 10)

    for i in range(tests_number):
        g = generate_test()

        test_algorithm(g)

