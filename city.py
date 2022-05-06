from dis import show_code
import osmnx as ox
from attr import attributes
import pandas as pd
import networkx as nx
from staticmap import *
from typing import Optional, List, Tuple, Union
import matplotlib.pyplot as plt
from haversine import *
from PIL import Image
import PIL
import os
from metro import*

CityGraph = nx.Graph

OsmnxGraph = nx.MultiDiGraph

Coord = (float, float)  # (latitude, longitude)


def get_osmnx_graph() -> OsmnxGraph:
    if os.path.exists('filename1.osm'):
        return load_osmnx_graph('filename1.osm')
    else:
        g = ox.graph_from_place('Barcelona, España', network_type='walk')
        save_osmnx_graph(g, 'filename1.osm')
        return g


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    ox.save_graphml(g, filename)


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    return ox.load_graphml(filename)


def add_access_to_closest_streets(g: CityGraph) -> None:
    dist = float('inf')
    closest_street = ""
    for access in g.nodes.data():
        if access[1]['type'] == 'Access':
            for street in g.nodes.data():
                d = haversine(access[1]['pos'], street[1]['pos'])
                if street[1]['type'] == 'Street' and d < dist:
                    dist = d
                    closest_street = street[0]
            att = {
                'type': 'Street', 
                'dist': dist, 
                'speed': 6/(3.6),
                'weight': dist*(1/6), 

            }
            g.add_edge(access[0], closest_street, **att)
            closest_street = ""
            dist = float('inf')


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:
    g: CityGraph = CityGraph()
    for n1 in g1.nodes.data():
        att = {
            'type': 'Street',
            'pos': (n1[1]['x'], n1[1]['y'])
        }
        g.add_node(n1[0], **att)
    for n2 in g2.nodes.data():
        g.add_node(n2[0], **n2[1])
    for e1 in g1.edges.data():
        if e1[0] != e1[1]:
            att1 = {
                'type': 'Street',
                'weight': float(e1[2]['length'])*(1/6),
                'dist': e1[2]['length'] / 1000,
                'speed': 6/(3.6),
            }
            g.add_edge(e1[0], e1[1], **att1)
    for e2 in g2.edges.data():
        if e2[0] != e2[1]:
            g.add_edge(e2[0], e2[1], **e2[2])

    add_access_to_closest_streets(g)

    return g


NodeID = Union[int, str]
Path = List[NodeID]


def find_closest_node(ox_g: OsmnxGraph, coo: Coord) -> NodeID:
    node = ox.distance.nearest_nodes(ox_g, coo[0], coo[1])
    return node


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    n_src: NodeID = find_closest_node(ox_g, src)
    n_dst: NodeID = find_closest_node(ox_g, dst)
    return nx.shortest_path(g, source=n_src, target=n_dst, weight='weight', method='dijkstra')


def show1(g: CityGraph) -> None:
    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False)
    plt.show()


def plot1(g: CityGraph, filename: str) -> None:
    m = StaticMap(680, 600, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    for index, node in g.nodes(data=True):
        coord = (node['pos'])
        if node['type'] == 'Street':
            marker_node = CircleMarker(coord, 'green', 1)
        else:
            marker_node = CircleMarker(coord, 'red', 1)
        m.add_marker(marker_node)
    for n1 in g.edges(data=True):
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        if g.edges[n1[0], n1[1]]['type'] == 'Street':
            line = Line(coord, 'yellow', 1)
        else:
            line = Line(coord, 'blue', 1)
        m.add_line(line)
    image = m.render()
    image.save(filename, quality=100)


colors : dict = {'L1': 'red', 'L2': 'purple', 'L3': 'green', 'L4': 'yellow', 'L5': 'blue', 
                       'L6': 'violet', 'L7': 'brown', 'L8': 'pink', 'L9S': 'orange', 'L9N': 'orange',
                                'L10N': 'cyan', 'L10S': 'cyan', 'L11': 'lime'}

def plot_path(g: CityGraph, p: Path, src: Coord, dst: Coord, filename: str) -> None:
    m = StaticMap(550, 550, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    i = 0
    m.add_line(Line((src, g.nodes[p[0]]['pos']), 'black', 5))
    while i < len(p)-1:
        coord = g.nodes[p[i]]['pos']
        next_coord = g.nodes[p[i+1]]['pos']
        marker_node = CircleMarker(coord, 'blue', 5)
        # m.add_marker(marker_node)
        if g.edges[p[i], p[i+1]]['type'] != 'tram':
            line = Line((coord, next_coord), 'black', 5)
        else:
            color = colors[g.edges[p[i], p[i+1]]['line']]
            line = Line((coord, next_coord), color, 5)
        m.add_line(line)
        i = i + 1
    m.add_line(Line((dst, g.nodes[p[-1]]['pos']), 'black', 5))
    image = m.render()
    image.save(filename, quality=100)

def time(g: CityGraph, p: Path) -> float: 
    i = 0
    distancia_total = 0.0
    velocitat_mitjana = 0.0
    while i < len(p)-1:
        distancia_total = distancia_total + float(g.edges[p[i], p[i+1]]['dist'])
        velocitat_mitjana = velocitat_mitjana + g.edges[p[i], p[i+1]]['speed']
        i = i + 1
    velocitat_mitjana = (velocitat_mitjana/(len(p)-1))
    distancia_total = distancia_total*1000
    time = (distancia_total)/(velocitat_mitjana)
    return time
    
def exec() -> None:
    g1 = get_osmnx_graph()
    g2 = get_metro_graph()
    g = build_city_graph(g1, g2)
    # show1(g)
    # plot1(g,'filename.png')
    src = (2.1231079101562504, 41.389945964560695)
    dst = (2.1917724609375004, 41.398960290742316)
    s = find_path(g1, g, src, dst)
    print(s)
    plot_path(g, s, src, dst,'filename.png')
    t = time(g, s)
    print(t)
