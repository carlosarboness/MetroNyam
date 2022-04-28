
import pandas as pd
import networkx as nx
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt

MetroGraph = nx.Graph

def get_metro_graph() -> MetroGraph:
    metro =  MetroGraph() 
    lst_stations: Stations = read_stations()
    for stat in lst_stations: 
        metro.add_node(stat._name, pos=stat._location)
    return metro

location = Tuple[float, float]

class Station:
    _name: str
    _line: Tuple[str, int]
    _servei: Tuple[str, str]
    _color: str
    _location: location

    def __init__(self, name: str, line: Tuple[str, int], servei: Tuple[str, str], color: str, geometry: location) -> None:
        self._name = name 
        self._line = line 
        self._servei = servei
        self._color = color
        self._location = geometry

class Access: 
    _name: str
    _station_name: str
    _accesstypte: bool  # true if accessible, false if not
    _location: location

    def __init__(self, name: str, station_name: str, accesstype: str, geometry: location) -> None:
        self._name = name 
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
        s = Station(row['NOM_ESTACIO'], (row['NOM_LINIA'], int(row['ORDRE_ESTACIO'])), 
                        (row['ORIGEN_SERVEI'], row['DESTI_SERVEI']), row['COLOR_LINIA'],
                        point(row['GEOMETRY']))
        Stations_list.append(s)
    return Stations_list

def read_accesses() -> Accesses: 
    df = pd.read_csv('acc.csv')
    Accesses_list: Accesses = []
    for index, row in df.iterrows():
        a = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_TIPUS_ACCESSIBILITAT'], point(row['GEOMETRY']))
        Accesses_list.append(a)
    return Accesses_list

def point(geomety: str) -> location:  
    word: list[str] = geomety.split()
    return (float(word[1].replace("(", "")), float(word[2].replace(")", "")))

def exec() -> None: 
    metro = get_metro_graph()
    nx.draw(metro, nx.get_node_attributes(metro, 'pos'), with_labels=True, node_size=0)
    plt.savefig("path.png")

exec()