from Tests.testDataReader import readTest
from Tests.testParametrizedAlgo import testParametrizedAlgoriths
from Tests.testExponentialAlgo import testExponentialAlgorithms

if __name__ == '__main__':
    filename = input("Enter test file name: ")
    G, edges = readTest(filename)

    testParametrizedAlgoriths(G, edges)
    testExponentialAlgorithms(G)
