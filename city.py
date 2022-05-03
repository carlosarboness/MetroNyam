
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
    for access in g.nodes(data=True):
        if access[1]['type'] == 'Access':
            for street in g.nodes(data=True):
                if street[1]['type'] == 'Street' and haversine(street[1]['pos'], access[1]['pos']) < dist:
                    dist = haversine(street[1]['pos'], access[1]['pos'])
                    n1 = street[1]
                    n2 = access[1]
        att4 = {
            'type': 'Street',
            #'length': haversine(n1[1]['pos'], n2[1]['pos'])
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

    add_access_streets(g)

    return g

def exec() -> None: 
    g1 = get_osmnx_graph()
    g2 = get_metro_graph()
    g = build_city_graph(g1, g2)
    show(g)

exec()