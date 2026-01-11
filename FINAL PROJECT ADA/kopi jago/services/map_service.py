import folium
from data.locations import locations

def create_map(start_coords, route, driver_name):
    m = folium.Map(location=start_coords, zoom_start=12)
    folium.Marker(start_coords, popup=f"{driver_name} Start",
                  icon=folium.Icon(color="blue")).add_to(m)
    

    path = [start_coords]
    for stop in route:
        lat, lon, _ = locations[stop]
        folium.Marker((lat, lon), popup=stop,
                      icon=folium.Icon(color="red")).add_to(m)
        path.append((lat, lon))

    folium.PolyLine(path).add_to(m)
    return m._repr_html_()
