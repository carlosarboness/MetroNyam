
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

CityGraph = nx.Graph

OsmnxGraph = nx.MultiDiGraph

def get_osmnx_graph() -> OsmnxGraph:
    G = ox.graph_from_place('Barcelona, España' , network_type='drive')
    ox.plot_graph(G)


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    ox.save_load.save_graph_osm(g, filename=filename)


def exec() -> None: 
    g = get_osmnx_graph()
    save_osmnx_graph(g, "filename1.png")
exec()