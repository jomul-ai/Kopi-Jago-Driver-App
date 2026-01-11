from flask import Flask, render_template, request
from datetime import datetime

from algorithms.route_optimizer import assign_route
from services.map_service import create_map
from algorithms.mst import build_graph, prim_mst
from data.locations import locations

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    lat = float(request.form["lat"])
    lon = float(request.form["lon"])
    start = request.form["start"]
    end = request.form["end"]

    t1 = datetime.strptime(start, "%H:%M")
    t2 = datetime.strptime(end, "%H:%M")
    working_hours = (t2 - t1).seconds / 3600

    route, dist, revenue = assign_route(lat, lon, working_hours)
    map_html = create_map((lat, lon), route, name)

    mst_edges, mst_distance = [], 0
    if len(route) > 1:
        filtered = {k: locations[k] for k in route}
        graph = build_graph(filtered)
        mst_edges, mst_distance = prim_mst(graph)

    return render_template(
        "result.html",
        name=name,
        start=start,
        end=end,
        route=route,
        dist=dist,
        revenue=revenue,
        map_html=map_html,
        locations=locations,
        mst_edges=mst_edges,
        mst_distance=mst_distance
    )

@app.route("/navigate", methods=["POST"])
def navigate():
    route = request.form.getlist("route")

    if not route:
        return "No route"

    first = route[0]
    lat, lon, _ = locations[first]

    return render_template(
        "navigate.html",
        stop=first,
        lat=lat,
        lon=lon
    )

if __name__ == "__main__":
    app.run(debug=True)
