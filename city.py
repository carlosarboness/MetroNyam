
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

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: 
    g = CityGraph = CityGraph()
    for n1 in g1.nodes(): 
        g.add_node(n1)
    for n2 in g2.nodes(): 
        g.add_node(n2)
    for e1 in g1.edges(): 
        g.add_edge(e1)
    for e2 in g2.edges(): 
        g.add_edge(e2)

def exec() -> None: 
    g1 = get_osmnx_graph()
    g2 = get_metro_graph()
    g = build_city_graph(g1, g2)
    show(g)

exec()