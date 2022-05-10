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
from metro import *
import pickle

CityGraph = nx.Graph

OsmnxGraph = nx.MultiDiGraph

Coord = (float, float)  # (latitude, longitude)


def get_osmnx_graph() -> OsmnxGraph:
    if not os.path.exists('barcelona.pickle'):
        bcn_grf: OsmnxGraph = ox.graph_from_place('Barcelona, España', network_type='walk', simplify = True)
        save_osmnx_graph(bcn_grf, 'barcelona.pickle')
    return load_osmnx_graph('barcelona.pickle')


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    pickle_out = open(filename,'wb')
    pickle.dump(g, pickle_out)
    pickle_out.close()


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    pickle_in = open(filename,'rb')
    bcn_grf: OsmnxGraph = pickle.load(pickle_in)
    pickle_in.close()
    return bcn_grf


def access_to_closest_streets(g1: OsmnxGraph, g2: MetroGraph) -> list:
    lst_x = []
    lst_y = []
    nodes =[]
    for n in g2.nodes.data():
        if n[1]['type'] == 'Access':
            lst_x.append(n[1]['pos'][0])
            lst_y.append(n[1]['pos'][1])
            nodes.append(n[0])
    street, dist = ox.distance.nearest_nodes(g1, lst_x, lst_y, return_dist = True)
    access_to_street: list = zip(nodes, street, dist)
    return access_to_street


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:
    g: CityGraph = CityGraph()

    access_to_street: list = access_to_closest_streets(g1, g2)

    for n in g1.nodes.data():
        att = {
            'type': 'Street',
            'pos': (n[1]['x'], n[1]['y'])
        }
        g.add_node(n[0], **att)
    for n in g2.nodes.data():
        g.add_node(n[0], **n[1])
    for e in g1.edges.data():
        if e[0] != e[1]:
            att1 = {
                'type': 'Street',
                'weight': float(e[2]['length'])*(1/6),
                'dist': e[2]['length'] / 1000,
                'speed': 6/(3.6),
            }
            g.add_edge(e[0], e[1], **att1)
    for e in g2.edges.data():
        if e[0] != e[1]:
            g.add_edge(e[0], e[1], **e[2])
    for e in access_to_street:
        att = {
                'type': 'Street', 
                'dist': e[2]/1000, 
                'speed': 6/(3.6),
                'weight': e[2]/1000*(1/6), 
            }
        g.add_edge(e[0], e[1], **att)


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
    show1(g)
    plot1(g, 'barcelona.png')

