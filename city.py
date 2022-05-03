
from dis import show_code
import osmnx as ox 
from attr import attributes
import pandas as pd
import networkx as nx
from staticmap import *
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
from haversine import *
from PIL import Image
import PIL
import os
from metro import*

CityGraph = nx.Graph

OsmnxGraph = nx.MultiDiGraph

Coord = (float, float) 

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

def add_access_streets(g: CityGraph) -> None:
    dist = float('inf')
    n1 = ""
    n2 = ""
    for access in g.nodes.data():
        if access[1]['type'] == 'Access':
            for street in g.nodes.data():
                if street[1]['type'] == 'Street' and haversine(street[1]['pos'], access[1]['pos']) < dist:
                    haversine(street[1]['pos'], access[1]['pos'])
                    n1 = street[0]
                    n2 = access[0]
        att4 = {
            'type': 'Street'
        }
        g.add_edge(n1, n2, **att4) 

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

    #add_access_streets(g)

    return g

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


def exec() -> None: 
    g1 = get_osmnx_graph()
    g2 = get_metro_graph()
    g = build_city_graph(g1, g2)
    show1(g)
    plot1(g,'filename.png')
   
exec()