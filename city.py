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
            g.add_edge(access[0], closest_street, type='Street')
            closest_street = ""
            dist = float('inf')


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: 
    g : CityGraph = CityGraph()
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
                'length': e1[2]['length']
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
    node = ox.distance.nearest_nodes(ox_g, coo[0], coo[1], return_dist = True)
    return node[0] 

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    n_src: NodeID = find_closest_node(ox_g, src)
    n_dst: NodeID = find_closest_node(ox_g, dst)
    return nx.shortest_path(g, source=n_src, target=n_dst, method='dijkstra')

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
        if g.edges[n1[0],n1[1]]['type'] == 'Street': 
            line = Line(coord, 'yellow', 1)
        else: 
            line = Line(coord, 'blue', 1)
        m.add_line(line)
    image = m.render()
    image.save(filename, quality=100)

def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    m = StaticMap(550, 550, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    i = 0
    while i < len(p)-1:
        coord = g.nodes[p[i]]['pos']
        next_coord = g.nodes[p[i+1]]['pos']
        marker_node = CircleMarker(coord, 'blue', 5)
        #m.add_marker(marker_node)
        if g.edges[p[i], p[i+1]]['type'] == 'Street': 
            line = Line((coord, next_coord), 'black', 5)
        else: 
            line = Line((coord, next_coord), 'red', 5)
        m.add_line(line)
        i = i + 1
    image = m.render()
    image.save(filename, quality=100)

def exec() -> None: 
    g1 = get_osmnx_graph()
    g2 = get_metro_graph()
    g = build_city_graph(g1, g2)
    #show1(g)
    #plot1(g,'filename.png')
    src = (2.1677043,41.374507)
    dst = (2.1411482,41.3738284)
    s = find_path(g1, g, src, dst)
    print(s)
    plot_path(g, s, 'filename.png')
   
exec()