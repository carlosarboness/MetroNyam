import osmnx as ox
import os
from typing_extensions import TypeAlias
import networkx as nx
from staticmap import *
from typing import List, Type, Union, Tuple, Optional
import matplotlib.pyplot as plt
from haversine import *
import metro as mt
import pickle


CityGraph: TypeAlias = nx.Graph


OsmnxGraph: TypeAlias = nx.MultiDiGraph


Coord: TypeAlias = Tuple[float, float]   # (latitude, longitude)


def get_osmnx_graph() -> OsmnxGraph:
    """ Returns the streets graph of Barcelona city in pickle format, if the
    graph has already been created it reads the graph from the indicated
    file """

    if not os.path.exists('barcelona.pickle'):
        bcn_grf: OsmnxGraph = ox.graph_from_place('Barcelona, España', network_type='walk', simplify=True)
        save_osmnx_graph(bcn_grf, 'barcelona.pickle')
    return load_osmnx_graph('barcelona.pickle')


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """ Writes the graph g in pickle format on the file filename """

    pickle_out = open(filename, 'wb')
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """ Returns the graph written in the file filename in pickle format.
    Prec: the graph has already been writed in the file """

    pickle_in = open(filename, 'rb')
    bcn_grf: OsmnxGraph = pickle.load(pickle_in)
    pickle_in.close()
    return bcn_grf


def access_to_closest_streets(g1: OsmnxGraph, g2: mt.MetroGraph) -> list:
    """ Returns a list where every element is in this format: (node1, node2,
    distance from node1 to node2). Node1 is always an access, and node2 is
    it's closest street from the g1 graph. In this way later we only have to
    iterate this list and create edges from node1 to node2, adding the distance
    to the attributes """

    acces_X_coordinates: list[float] = []
    acces_Y_coordinates: list[float] = []
    accesses: list[str] = []
    for n in g2.nodes.data():
        if n[1]['type'] == 'Access':
            acces_X_coordinates.append(n[1]['pos'][0])
            acces_Y_coordinates.append(n[1]['pos'][1])
            accesses.append(n[0])
    street, dist = ox.distance.nearest_nodes(g1, acces_X_coordinates, acces_Y_coordinates, return_dist=True)
    return zip(accesses, street, dist)


def get_attributes_from_osmnx_nodes(n: Tuple[str, dict]) -> dict:
    """ Returns the attributes from the node n, that is a node from the osmnx
    graph. We save the type ofnode it is (Street) and the coordinates of the
    node (pos) """

    return {'type': 'Street',
            'pos': (n[1]['x'], n[1]['y'])}


def get_attributes_from_osmnx_edges(e: Tuple[str, str, dict]) -> dict:
    """ Returns the attributes from the edge e, that is an edge from the osmnx
    graph. We save the type of edge it is (Street), the weight of the edge
    (is the edge length - that is the length of the street - times 1/6, that is
    the inverse of the mean walking speed  - because we need that as more speed
    less weight -, the distance of the edge (street) in metres and also the
    meanwalking speed (6km/h) in metres per second (we have to divide per 3.6).
    """

    return {'type': 'Street',
            'weight': e[2]['length']*(1/6),
            'dist': e[2]['length'] / 1000,
            'speed': 6/(3.6),
            'color': 'black'}


def get_attributes_from_acces_to_street(e: Tuple[str, str, dict]) -> dict:
    """ Returns the attributes from the edge e, that is an edge joins an access
    e[0] to it closest street e[1]. We save the type (street), the distance
    between the two nodes (dist) in metres, the mean walking speed (6km/h) in
    metres per second (we have to divide per 3.6) and the weight of the edge
    (is the edge length times 1/6, that is the inverse of the mean walking
    speed - because we need that as more speed less weight - """

    return {'type': 'Street',
            'dist': e[2]/1000,
            'speed': 6/(3.6),
            'weight': e[2]/1000*(1/6),
            'color': 'black'}


def build_city_graph(g1: OsmnxGraph, g2: mt.MetroGraph) -> CityGraph:
    """ Returns a networkx graph, that is the merged graph of the streets of
    Barcelona (g1) and the graph of  the metro lines (g2). We first create the
    city graph that is g, then we create a list joining every access in the
    metro to it's closest street in the g1 graph (and with the distance between
    them). We iterate the nodes from the g1 graph (streets) and save them with
    the attributes we selected. We to the same with the edges of the g1 graph
    (streets), and then the same with the edges of the list that we created in
    first place """

    g: CityGraph = g2
    access_to_street: list = access_to_closest_streets(g1, g2)

    for n in g1.nodes.data():
        att: dict = get_attributes_from_osmnx_nodes(n)
        g.add_node(n[0], **att)

    for e in g1.edges.data():
        if e[0] != e[1]:  # cheking for loops in nodes
            att: dict = get_attributes_from_osmnx_edges(e)
            g.add_edge(e[0], e[1], **att)

    for e in access_to_street:
        att: dict = get_attributes_from_acces_to_street(e)
        g.add_edge(e[0], e[1], **att)

    return g


NodeID: TypeAlias = Union[int, str]


Path: TypeAlias = List[NodeID]


def find_closest_node(ox_g: OsmnxGraph, coo: Coord) -> NodeID:
    """ Returns the closest node id to the coordinates coo of the ox_g graph"""

    return ox.distance.nearest_nodes(ox_g, coo[0], coo[1])


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """ Returns the shortest path (we use the weight of nodes) between the Node
    n_src, that is the closest node to the src -origin- coordinates, and the
    Node n_dst, that is the closest node to the dst -destiny- coordinates """

    n_src: NodeID = find_closest_node(ox_g, src)
    n_dst: NodeID = find_closest_node(ox_g, dst)
    return nx.shortest_path(g, source=n_src, target=n_dst, weight='weight', method='dijkstra')


def show(g: CityGraph) -> None:
    """ Shows in an interactive screen the graph (nodes and edges) from g, that
    is the graph that contains both the graph of the metro and streets of
    Barcelona """

    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False)
    plt.show()


def paint_nodes(g: CityGraph, m: StaticMap) -> None:
    """ Paints all the nodes from the graph g in the StaticMap m, if the node
    is a street we paint it in color green, if is a metro node in color red """

    for index, node in g.nodes.data():
        coord = (node['pos'])
        if node['type'] == 'Street':
            marker_node = CircleMarker(coord, 'green', 1)
        else:
            marker_node = CircleMarker(coord, 'red', 1)
        m.add_marker(marker_node)


def paint_edges(g: CityGraph, m: StaticMap) -> None:
    """ Paints all the edges from the graph g in the StaticMap m, if the edge
    is a street we paint it in color yellow, if is a metro edge in color blue
    """

    for n1 in g.edges.data():
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        if g.edges[n1[0], n1[1]]['type'] == 'Street':
            line = Line(coord, 'yellow', 1)
        else:
            line = Line(coord, 'blue', 1)
        m.add_line(line)


def plot(g: CityGraph, filename: str) -> None:
    """ Saves the image of the citygraph in the file -filename-. We iterate
    all the nodes, and  edges from the graph g and colour them with the
    image of the barcelona map at the background """

    url: str = "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
    m: StaticMap = StaticMap(1000, 1000, url_template=url)

    paint_nodes(g, m)
    paint_edges(g, m)

    image = m.render()
    image.save(filename, quality=1000)


def paint_path(g: CityGraph, m: StaticMap, p: Path) -> None:
    """ Paints the edges that connect the nodes from g contained in p in the
    StaticMap m. If it's a metro edge we paint it with the color of the metro
    line we are using, everthing else we painted in black, simbolizing we are
    walking"""

    for i in range(0, len(p)-1):

        coord = g.nodes[p[i]]['pos']
        next_coord = g.nodes[p[i+1]]['pos']
        color = g.edges[p[i], p[i+1]]['color']
        line = Line((coord, next_coord), color, 5)
        m.add_line(line)


def plot_path(g: CityGraph, p: Path, src: Coord, dst: Coord, filename: str) -> None:
    """ Saves in the file <filename> the painted path p that goes from the src
    coordinates to the dst coordinates. The nodes are from g and the path is
    painted with an image of the Barcelona map at the background"""

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
    """ Returns the time (in minutes) that going from the first node of path
    to the last one is going to take. We sum the time is going to take every
    edge of the path and return the result"""

    time = 0.0
    for i in range(0, len(p)-1):
        edge_dist = float(g.edges[p[i], p[i+1]]['dist'])*1000
        speed = float(g.edges[p[i], p[i+1]]['speed'])
        time += (edge_dist/speed)

    return time/60
    