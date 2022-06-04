import os
import pickle
import metro as mt
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from typing_extensions import TypeAlias
from typing import List, Union, Tuple
from staticmap import *
from haversine import *


CityGraph: TypeAlias = nx.Graph


OsmnxGraph: TypeAlias = nx.MultiDiGraph


Coord: TypeAlias = Tuple[float, float]   # (latitude, longitude)


def get_osmnx_graph() -> OsmnxGraph:
    """Returns the streets graph of Barcelona city in pickle format"""

    if not os.path.exists('barcelona.pickle'):
        bcn_grf: OsmnxGraph = ox.graph_from_place('Barcelona, España', network_type='walk', simplify=True)
        save_osmnx_graph(bcn_grf, 'barcelona.pickle')
    return load_osmnx_graph('barcelona.pickle')


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """Writes the graph g in pickle format on the file filename"""

    pickle_out = open(filename, 'wb')
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """Returns the graph written in the file filename in pickle format.
    Prec: the graph has already been writed in the file"""

    pickle_in = open(filename, 'rb')
    bcn_grf: OsmnxGraph = pickle.load(pickle_in)
    pickle_in.close()
    return bcn_grf


def access_to_closest_streets(g1: OsmnxGraph, g2: mt.MetroGraph) -> list:
    """Returns a list where every element is in this format: (node1, node2,
    distance from node1 to node2)"""

    acces_X_coordinates: list[float] = []  # list of accesses' latitude
    acces_Y_coordinates: list[float] = []  # list of accesses' longitude
    accesses: list[str] = []  # list of accesses' id's

    for n in g2.nodes.data():
        if n[1]['type'] == 'Access':
            acces_X_coordinates.append(n[1]['pos'][0])
            acces_Y_coordinates.append(n[1]['pos'][1])
            accesses.append(n[0])

    streets, dist = ox.distance.nearest_nodes(g1, acces_X_coordinates, acces_Y_coordinates, return_dist=True)
    return zip(accesses, streets, dist)


def get_attributes_from_osmnx_nodes(n: Tuple[str, dict]) -> dict:
    """Returns the attributes from the node n, which is an OsmnxGraph node"""

    return {'type': 'Street',
            'pos': (n[1]['x'], n[1]['y'])}


def get_attributes_from_osmnx_edges(e: Tuple[str, str, dict]) -> dict:
    """Returns the attributes from the edge e, which is an OsmnxGraph edge"""

    dist: float = e[2]['length']  # distance in meters
    return {'type': 'Street',
            'dist': dist,
            'speed': 6/(3.6),  # mean walking speed (6km/h) in m/s
            'weight': dist/mt.WALK_SPEED,  # distance divided by speed
            'color': 'black'}  # the color black means that it is walking


def get_attributes_from_acces_to_street(e: Tuple[str, str, float]) -> dict:
    """Returns the attributes from the edge e, which joins an access
    e[0] to it closest street e[1] with distance e[2]
    Prec: distance e[2] must be in meters"""

    return {'type': 'Street',
            'dist': e[2],  # distance in meters
            'speed': mt.WALK_SPEED,
            'weight': e[2]/mt.WALK_SPEED,  # distance divided by speed
            'color': 'black'}  # the color black means that it is walking


def build_city_graph(g1: OsmnxGraph, g2: mt.MetroGraph) -> CityGraph:
    """Given an OsmnxGraph g1 and a MetroGraph g2, returns a CityGraph
    graph which is the merged graph of g1 and g2"""

    # copy all the nodes and edges of g2 to g
    g: CityGraph = g2

    # add every node of g1 to g
    for n in g1.nodes.data():
        att: dict = get_attributes_from_osmnx_nodes(n)
        g.add_node(n[0], **att)

    # add every edge of g1 to g
    for e in g1.edges.data():
        if e[0] != e[1]:  # cheking for loops in nodes
            att: dict = get_attributes_from_osmnx_edges(e)
            g.add_edge(e[0], e[1], **att)

    # add edges between cloesest nodes from g1 to g2
    access_to_street: list = access_to_closest_streets(g1, g2)
    for e in access_to_street:
        att: dict = get_attributes_from_acces_to_street(e)
        g.add_edge(e[0], e[1], **att)

    return g


NodeID: TypeAlias = Union[int, str]


Path: TypeAlias = List[NodeID]


def find_closest_node(ox_g: OsmnxGraph, coo: Coord) -> NodeID:
    """Returns the closest node id to the Coord coo of the ox_g graph"""

    return ox.distance.nearest_nodes(ox_g, coo[0], coo[1])


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """Returns the shortest path from the Coord src to the Coord dst"""

    n_src: NodeID = find_closest_node(ox_g, src)  # cloesest node to the Coord src
    n_dst: NodeID = find_closest_node(ox_g, dst)  # cloesest node to the Coord dst
    return nx.shortest_path(g, source=n_src, target=n_dst, weight='weight', method='dijkstra')


def show(g: CityGraph) -> None:
    """Shows in an interactive screen the CityGraph (nodes and edges) g"""

    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False)
    plt.show()


def paint_nodes(g: CityGraph, m: StaticMap) -> None:
    """Paints all the nodes from the graph g in the StaticMap m,
    the street nodes in green and the metro nodes in red"""

    for index, node in g.nodes.data():
        coord = (node['pos'])
        if node['type'] == 'Street':
            marker_node = CircleMarker(coord, 'green', 1)
        else:
            marker_node = CircleMarker(coord, 'red', 1)
        m.add_marker(marker_node)


def paint_edges(g: CityGraph, m: StaticMap) -> None:
    """Paints all the edges from the graph g in the StaticMap m,
    the street edges in yellow and the metro edges in blue"""

    for n1 in g.edges.data():
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        if g.edges[n1[0], n1[1]]['type'] == 'Street':
            line = Line(coord, 'yellow', 1)
        else:
            line = Line(coord, 'blue', 1)
        m.add_line(line)


def plot(g: CityGraph, filename: str) -> None:
    """Saves the image of the CityGraph in the file <filename>"""

    # we get the openstreetmap to be the background
    url: str = "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
    m: StaticMap = StaticMap(1000, 1000, url_template=url)

    paint_nodes(g, m)
    paint_edges(g, m)

    image = m.render()
    image.save(filename, quality=1000)


def paint_path(g: CityGraph, m: StaticMap, p: Path) -> None:
    """Paints the edges that connect the nodes from g contained in p in the
    StaticMap m"""

    for i in range(0, len(p)-1):

        coord = g.nodes[p[i]]['pos']
        next_coord = g.nodes[p[i+1]]['pos']
        color = g.edges[p[i], p[i+1]]['color']
        line = Line((coord, next_coord), color, 5)
        m.add_line(line)


def plot_path(g: CityGraph, p: Path, src: Coord, dst: Coord, filename: str) -> None:
    """Saves in the file <filename> the painted path p that goes from the src
    coordinates to the dst coordinates."""

    url: str = "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
    m: StaticMap = StaticMap(1000, 1000, url_template=url)

    m.add_marker(CircleMarker(src, 'white', 10))
    m.add_marker(CircleMarker(src, 'blue', 6))

    # we join the origin with the first path node
    m.add_line(Line((src, g.nodes[p[0]]['pos']), 'black', 5))

    paint_path(g, m, p)

    # we join the destiny with the last path node
    m.add_marker(CircleMarker(dst, 'white', 10))

    m.add_marker(CircleMarker(dst, 'red', 6))
    m.add_line(Line((dst, g.nodes[p[-1]]['pos']), 'black', 5))

    image = m.render()
    image.save(filename, quality=100)


def time(g: CityGraph, p: Path) -> float:
    """Returns the time (in minutes) that is going to take the path p"""

    time: float = 0.0

    # sum the time that is going to take every edge
    for i in range(0, len(p)-1):
        edge_dist = float(g.edges[p[i], p[i+1]]['dist'])
        speed = float(g.edges[p[i], p[i+1]]['speed'])
        time += (edge_dist/speed)

    return time/60
