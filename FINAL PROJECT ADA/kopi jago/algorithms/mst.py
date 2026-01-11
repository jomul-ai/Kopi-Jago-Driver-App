from algorithms.route_optimizer import haversine
import heapq
def prim_mst(graph):
    start = next(iter(graph))
    visited = set([start])
    mst_edges = []
    total_cost = 0

    pq = []
    for to, cost in graph[start].items():
        heapq.heappush(pq, (cost, start, to))

    while pq:
        cost, frm, to = heapq.heappop(pq)
        if to not in visited:
            visited.add(to)
            mst_edges.append((frm, to, round(cost, 2)))
            total_cost += cost

            for next_to, next_cost in graph[to].items():
                if next_to not in visited:
                    heapq.heappush(pq, (next_cost, to, next_to))

    return mst_edges, round(total_cost, 2)

def build_graph(locations):
    graph = {k: {} for k in locations}

    for a in locations:
        lat1, lon1, _ = locations[a]
        for b in locations:
            if a != b:
                lat2, lon2, _ = locations[b]
                graph[a][b] = haversine(lat1, lon1, lat2, lon2)

    return graph
import heapq