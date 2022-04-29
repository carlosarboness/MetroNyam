
from attr import attributes
import pandas as pd
import networkx as nx
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
from haversine import *

MetroGraph = nx.Graph

def get_metro_graph() -> MetroGraph:
    metro =  MetroGraph() 
    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()
    nom_linia = "qq"
    node_anterior = ""
    pos_anterior: location = (0, 0)
    for stat in lst_stations: 
        attributes = {
            'pos': stat._location, 
            'color': stat._color,
            'type': 'Station'
        }
        metro.add_node(stat._name, **attributes)
        if stat._line[0] != nom_linia: 
            nom_linia = stat._line[0]
        else: 
            att1 = {
                'weight': haversine(node_anterior._location, stat._location),
                'l':(node_anterior._location, stat._location),
                'type': 'access'
            }
            metro.add_edge(node_anterior._name, stat._name, **att1)
        node_anterior = stat
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
    path = nx.shortest_path(metro, source='Av. Carrilet', target='Fondo', weight='weight', method='dijkstra')
    print(path)
    n = len(path)
    for i in range(0, n-1): 
        metro.remove_edge(path[i], path[i+1])
        metro.add_edge(path[i], path[i+1], color='red')
    nx.draw(metro, nx.get_node_attributes(metro,'pos'), node_size=10, with_labels=False)
    plt.savefig("path.png")


exec()
