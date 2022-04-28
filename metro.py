import pandas as pd
import networkx
from typing import Optional, List, Tuple

def get_metro_graph() -> MetroGraph: 
    return

MetroGraph = networkx.Graph

class Location: 

    _location: str
    
    def __init__(self, location: str) -> None:
        self._location = location
    
    def get(self, i: int) -> str: 

        assert i == 1 or i == 2
        word: list[str] = self._location.split()
        if i == 1: 
            return word[i].pop(0)
        else: 
            return word[i].pop(-1)
        
class Station: 
    _name: str
    _line: Tuple[str, int]
    _servei: Tuple[str, str]
    _color: str
    _coord: Tuple[str, str]

    def __init__(self, name: str, line: Tuple[str, int], servei: Tuple[str, str], color: str) -> None:
        self._name = name 
        self._line = line 
        self._servei = servei
        self._color = color

class Access: 
    _name: str 
    _station_name: str 
    _accesstypte: bool #true if accessible, false if not
    _elevatrosnum: int 

    def __init__(self, name: str, station_name: str, accesstype: str, elevatorsnum: int) -> None:
        self._name = name 
        self._station_name = station_name 
        if accesstype == "Accessible": 
            self._accesstypte = True 
        else: 
            self._accesstypte = False 
        self._elevatrosnum = elevatorsnum


Stations = List[Station]

Accesses = List[Access]

def read_stations() -> Stations:
    df = pd.read_csv('stat.csv')
    Stations_list: Stations = []
    for index, row in df.iterrows():
        s = Station(row['NOM_ESTACIO'], (row['NOM_LINIA'], row['ORDRE_ESTACIO']), 
                        (row['ORIGEN_SERVEI'], row['DESTI_SERVEI']), row['COLOR_LINIA'])
        Stations_list.append(s)
    return Stations_list

def read_accesses() -> Accesses: 
    df = pd.read_csv('acc.csv')
    Accesses_list: Accesses = []
    for index, row in df.iterrows():
        a = Access(row['NOM_ACCES'], row['NOM_ESTACIO'], row['NOM_TIPUS_ACCESSIBILITAT'], row['NUM_ASCENSORS'])
        Accesses_list.append(a)
    return Accesses_list

def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...