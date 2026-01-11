from algorithms.distance import haversine
from config import *
from data.locations import locations

route_load = {k: 0 for k in locations}

def assign_route(start_lat, start_lon, working_hours):
    remaining = set(locations.keys())
    route = []
    current_lat = start_lat
    current_lon = start_lon
    remaining_time = working_hours
    total_distance = 0

    while remaining_time > 0:
        best_node = None
        best_score = -1
        best_dist = 0

        for name in remaining:
            lat, lon, demand = locations[name]
            dist = haversine(current_lat, current_lon, lat, lon)
            travel_time = dist / AVG_TRAVEL_SPEED

            if route_load[name] >= MAX_ROUTE_LOAD:
                continue
            if travel_time + SELLING_TIME_PER_STOP > remaining_time:
                continue

            profit = min(demand, AVG_CUPS_PER_HOUR * working_hours) * COFFEE_PRICE
            score = profit - (dist * 3000)

            if score > best_score:
                best_score = score
                best_node = name
                best_dist = dist

        if not best_node:
            break

        route_load[best_node] += 1
        route.append(best_node)
        remaining.remove(best_node)

        total_distance += best_dist
        remaining_time -= (best_dist / AVG_TRAVEL_SPEED + SELLING_TIME_PER_STOP)
        current_lat, current_lon, _ = locations[best_node]

    # realistic revenue per stop
    revenue = 0
    remaining_time = working_hours

    for stop in route:
        sell_time = min(SELLING_TIME_PER_STOP, remaining_time)

        cups_sold = min(
        locations[stop][2],
        AVG_CUPS_PER_HOUR * sell_time
    )

        revenue += cups_sold * COFFEE_PRICE
        remaining_time -= sell_time
    
    return route, round(total_distance, 2), int(revenue)