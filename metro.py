
from attr import attributes
import pandas as pd
import networkx as nx
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
from haversine import *

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

def add_nodes_and_edges_from_lines(metro: MetroGraph(), last_line: None, last_node, lst_stations) -> None: 
    for stat in lst_stations: 
        att1 = get_att_station(stat)
        metro.add_node((stat._name + " " + stat._line[0]), **att1)

        if stat._line[0] != last_line: 
            last_line = stat._line[0]
        else: 
            get_att_tram(stat, last_node)
            att2 = get_att_tram(stat, last_node)
            metro.add_edge(last_node._name + " " + last_node._line[0], (stat._name + " " + stat._line[0]), **att2)
        last_node = stat

def get_metro_graph() -> MetroGraph:
    metro =  MetroGraph() 
    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()
    add_nodes_and_edges_from_lines(metro, None, None, lst_stations)
    for access in lst_accesses: 
        metro.add_node(access._name, pos=access._location)
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

    def get_station_code(self) -> int:
        return self._station_code
    
    def get_name(self) -> str:
        return self._name
    
    def get_line(self) -> Tuple[str, int]:
        return self._line
    
    def get_servei(self) -> Tuple[str, str]:
        return self._servei
    
    def get_color(self) -> Tuple[str, int]:
        return self._line
    
    def get_location(self) -> location:
        return self._location

class Access:
    _name: str
    _station_code: int
    _station_name: str
    _accesstypte: bool  # true if accessible, false if not
    _location: location

    def __init__(self, name: str, station_code: int, station_name: str, accesstype: str, geometry: location) -> None:
        self._name = name 
        self._station_code = station_code
        self._station_name = station_name 
        if accesstype == "Accessible": 
            self._accesstypte = True 
        else: 
            self._accesstypte = False 
        self._location = geometry
    
    def get_name(self) -> str:
        return self._name

    def get_station_code(self) -> int:
        return self._station_code
    
    def get_acssesstype(self) -> bool:
        return self._accesstypte
    
    def get_location(self) -> location:
        return self._location


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
    return (float(word[2].replace(")", "")), float(word[1].replace("(", "")))

def exec() -> None: 
    metro = get_metro_graph()
    for node1, node2, data in metro.edges(data=True):
        print("dist", "(", node1, ") --> (", node2,") == ", data['weight'])
    path = nx.shortest_path(metro, source='Av. Carrilet L1', target='Fondo L1', weight='weight', method='dijkstra')
    print(path)
    n = len(path)
    for i in range(0, n-1): 
        metro.remove_edge(path[i], path[i+1])
        metro.add_edge(path[i], path[i+1], color='red')
    nx.draw(metro, nx.get_node_attributes(metro,'pos'), node_size=10, with_labels=False)
    plt.savefig("path.png")


exec()
