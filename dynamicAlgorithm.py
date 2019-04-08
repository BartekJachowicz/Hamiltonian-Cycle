from graph import Graph


def calculate_masks(sets):
    mask_set = {}
    for s in sets:
        mask = 0
        for i in s:
            mask += (2**i)
        mask_set[s] = mask
    return mask_set


def check_bit(mask, bit):
    return mask & (2**bit)


def dynamic_algorithm(graph):
    sets = graph.power_set()
    mask_set = calculate_masks(sets)

    vertex_list = graph.vertex_list()
    x = vertex_list[0]

    dp = [[False for i in range(len(vertex_list))] for j in range(len(sets))]

    for s in sets:
        if len(s) == 2 and x in s:
            if s[1] in graph.graph[x]:
                dp[mask_set[s]][s[1]] = True

    for s in sets:
        for v in s:
            for u in s:
                if u == v or v not in graph.graph[u]:
                    continue
                m = mask_set[s] - 2**v
                if dp[m][u]:
                    dp[mask_set[s]][v] = True
                    break

    for v in vertex_list:
        if dp[2**len(vertex_list) - 1][v] and x in graph.graph[v]:
            return True

    return False
