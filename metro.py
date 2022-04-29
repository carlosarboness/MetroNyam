
from attr import attributes
import pandas as pd
import networkx as nx
from staticmap import *
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
from haversine import *
from PIL import Image

MetroGraph = nx.Graph

def get_att_station(stat) -> dict: 
    attributes = {
            'type': 'Station',
            'name': stat._name,
            'line': stat._line[0],
            'pos': stat._location, 
            'color': stat._color,
        } 
    return attributes

def get_att_tram(stat, last_node) -> dict: 

    attributes = {
                'weight': haversine(last_node._location, stat._location),
                'line': stat._line[0],
                'color': stat._color,
                'type': 'tram'
            }
    return attributes

def get_att_accesses(stat, access) -> dict: 
    attributes = {
                'weight': haversine(stat._location, access._location),
                'pos': access._location,
                'color': stat._color,
                'accessibility': access._accesstype,
                'type': 'Access'
            }
    return attributes

def add_nodes_and_edges_from_lines(metro: MetroGraph(), last_line: None, last_node: None, lst_stations, lst_accesses) -> None: 
    i = 0
    for stat in lst_stations: 
        att1 = get_att_station(stat)
        metro.add_node((stat._name + " " + stat._line[0]), **att1)
        while stat._station_code == lst_accesses[i]._station_code: 
            att2 = get_att_accesses(stat, lst_accesses[i])
            metro.add_node(lst_accesses[i]._name, **att2)
            #metro.add_edge((stat._name + " " + stat._line[0]), lst_accesses[i]._name)
            i = i + 1
        if stat._line[0] != last_line: 
            last_line = stat._line[0]
        else: 
            att3 = get_att_tram(stat, last_node)
            metro.add_edge(last_node._name + " " + last_node._line[0], (stat._name + " " + stat._line[0]), **att3)
        last_node = stat

def get_metro_graph() -> MetroGraph:
    metro =  MetroGraph() 
    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()
    add_nodes_and_edges_from_lines(metro, None, None, lst_stations, lst_accesses)
    return metro

location = Tuple[float, float]

class Station:
    _station_code: int
    _name: str
    _line: Tuple[str, int]
    _servei: Tuple[str, str]
    _color: str
    _location: location

    def __init__(self, station_code: int, name: str, line: Tuple[str, int], servei: Tuple[str, str], color: str, geometry: location) -> None:
        self._station_code = station_code
        self._name = name 
        self._line = line 
        self._servei = servei
        self._color = color
        self._location = geometry

class Access:
    _name: str
    _station_code: int
    _station_name: str
    _accesstype: str 
    _location: location

    def __init__(self, name: str, station_code: int, station_name: str, accesstype: str, geometry: location) -> None:
        self._name = name 
        self._station_code = station_code
        self._station_name = station_name 
        self._accesstype = accesstype
        self._location = geometry

Stations = List[Station]

Accesses = List[Access]

def read_stations() -> Stations:
    df = pd.read_csv('stat.csv')
    Stations_list: Stations = []
    for index, row in df.iterrows():
        s = Station(int(row['CODI_ESTACIO']), row['NOM_ESTACIO'], (row['NOM_LINIA'], 
                    int(row['ORDRE_ESTACIO'])), (row['ORIGEN_SERVEI'], row['DESTI_SERVEI']),
                    row['COLOR_LINIA'], point(row['GEOMETRY']))
        Stations_list.append(s)
    return Stations_list

def read_accesses() -> Accesses: 
    df = pd.read_csv('acc.csv')
    Accesses_list: Accesses = []
    for index, row in df.iterrows():
        a = Access(row['NOM_ACCES'], int(row['ID_ESTACIO']) , row['NOM_ESTACIO'], 
        row['NOM_TIPUS_ACCESSIBILITAT'], point(row['GEOMETRY']))
        Accesses_list.append(a)
    return Accesses_list

def point(geomety: str) -> location:  
    word: list[str] = geomety.split()
    return (float(word[1].replace("(", "")), float(word[2].replace(")", "")))

def show(g: MetroGraph) -> None:
    nx.draw(g, nx.get_node_attributes(g,'pos'), node_size=10, node_color="red", edge_color="blue", with_labels=False)
    plt.show()

def plot(g: MetroGraph, filename: str) -> None: 
    m = StaticMap(700, 800, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    coord = [[2.154007, 41.390205], [2.154007, 41.390205]]
    m.add_line(Line(coord, 'red', 0)) 
    image = m.render(center=[2.154007, 41.390205], zoom=11)
    image.save(filename)
    nx.draw(g, nx.get_node_attributes(g,'pos'), node_size=10, node_color="red", edge_color="blue", with_labels=False)
    plt.savefig('path.png', transparent=True)
    im1 = Image.open('path.png')
    im2 = Image.open('filename.png')
    im2.paste(im1)
    im2.show()

def exec() -> None: 
    metro = get_metro_graph()
    #show(metro)
    plot(metro, 'filename.png')

exec()