import math
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))
def build_graph(locations):
    graph = {k: {} for k in locations}

    for a in locations:
        lat1, lon1, _ = locations[a]
        for b in locations:
            if a != b:
                lat2, lon2, _ = locations[b]
                graph[a][b] = haversine(lat1, lon1, lat2, lon2)

    return graph
