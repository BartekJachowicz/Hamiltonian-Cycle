import itertools
import sys
import networkx as nx
import matplotlib


def nice_tree_decomp(graph):
    out = {}
    for node, neighbours in graph.items():
        vertex = list(node)
        if len(neighbours) == 1:
            for i in range(1, len(vertex)):
                out[frozenset(vertex[0:i])] = [frozenset(vertex[0:i + 1])]
            else:
                for N in neighbours:
                    Xj_Xi = [x for x in N if x not in vertex]
                    interXi_Xj = [x for x in N if x in vertex]
                    for i in range(len(interXi_Xj)):
                        # TODO
                        pass
    print(out)


def min_fill_in_heuristic(graph):
    if len(graph) == 0:
        return None

    min_fill_in_node = None

    min_fill_in = sys.maxsize

    # create sorted list of (degree, node)
    degree_list = [(len(graph[node]), node) for node in graph]
    degree_list.sort()

    # abort condition
    min_degree = degree_list[0][0]
    if min_degree == len(graph) - 1:
        return None

    for (_, node) in degree_list:
        num_fill_in = 0
        nbrs = graph[node]
        for nbr in nbrs:
            # count how many nodes in nbrs current nbr is not connected to
            # subtract 1 for the node itself
            num_fill_in += len(nbrs - graph[nbr]) - 1
            if num_fill_in >= 2 * min_fill_in:
                break

        num_fill_in /= 2  # divide by 2 because of double counting

        if num_fill_in < min_fill_in:  # update min-fill-in node
            if num_fill_in == 0:
                return node
            min_fill_in = num_fill_in
            min_fill_in_node = node

    return min_fill_in_node


def treewidth_decomposition(G, heuristic=min_fill_in_heuristic):
    graph = {n: set(G[n]) - {n} for n in G}

    # stack containing nodes and neighbors in the order from the heuristic
    node_stack = []

    # get first node from heuristic
    elim_node = heuristic(graph)
    while elim_node is not None:
        # connect all neighbours with each other
        nbrs = graph[elim_node]
        for u, v in itertools.permutations(nbrs, 2):
            if v not in graph[u]:
                graph[u].add(v)

        # push node and its current neighbors on stack
        node_stack.append((elim_node, nbrs))

        # remove node from graph
        for u in graph[elim_node]:
            graph[u].remove(elim_node)

        del graph[elim_node]
        elim_node = heuristic(graph)

    # the abort condition is met; put all remaining nodes into one bag
    decomp = nx.Graph()
    first_bag = frozenset(graph.keys())
    decomp.add_node(first_bag)

    treewidth = len(first_bag) - 1

    while node_stack:
        # get node and its neighbors from the stack
        (curr_node, nbrs) = node_stack.pop()

        # find a bag all neighbors are in
        old_bag = None
        for bag in decomp.nodes:
            if nbrs <= bag:
                old_bag = bag
                break

        if old_bag is None:
            # no old_bag was found: just connect to the first_bag
            old_bag = first_bag

        # create new node for decomposition
        nbrs.add(curr_node)
        new_bag = frozenset(nbrs)

        # update treewidth
        treewidth = max(treewidth, len(new_bag) - 1)

        # add edge to decomposition (implicitly also adds the new node)
        decomp.add_edge(old_bag, new_bag)

    out = {}
    for node in decomp.nodes:
        e = []
        for edge in decomp.edges:
            if edge[0] == node:
                e.append(edge[1])
            if edge[1] == node:
                e.append(edge[0])
        out[node] = e
    #print(out)
    print(list(decomp.nodes()))
    # nx.draw(decomp, with_labels=True)
    #nice_tree_decomp(out)
    return treewidth, decomp


def tree_decomposition():
    matplotlib.interactive(True)
    # G = {0: [1, 2], 1: [2, 3], 2: [3], 3: [4], 4: [0, 2]}
    G = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4, 5], 3: [1, 4], 4: [2, 3, 5], 5: [2, 4]}
    G_nx = nx.DiGraph()
    G_nx.add_nodes_from(G.keys())
    for k, v in G.items():
        G_nx.add_edges_from(([(k, t) for t in v]))
    return treewidth_decomposition(G)


if __name__ == '__main__':
    print(tree_decomposition())
