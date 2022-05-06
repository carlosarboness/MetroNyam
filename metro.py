from os import access
from attr import attributes
import pandas as pd
import networkx as nx
from staticmap import *
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
from haversine import *
from PIL import Image
import PIL

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
        return self._color

    def get_location(self) -> location:
        return self._location


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

    def get_name(self) -> str:
        return self._name

    def get_station_code(self) -> int:
        return self._station_code

    def get_station_name(self) -> str:
        return self._station_name

    def get_acssesstype(self) -> bool:
        return self._accesstype

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
        a = Access(row['NOM_ACCES'], int(row['ID_ESTACIO']), row['NOM_ESTACIO'],
        row['NOM_TIPUS_ACCESSIBILITAT'], point(row['GEOMETRY']))
        Accesses_list.append(a)
    return Accesses_list


def point(geomety: str) -> location:
    word: list[str] = geomety.split()
    return (float(word[1].replace("(", "")), float(word[2].replace(")", "")))


MetroGraph = nx.Graph


def get_att_station(stat: Station) -> dict:
    attributes = {
        'type': 'Station',
        'name': stat.get_name(),
        'line': stat.get_line()[0],
        'pos': stat.get_location(),
        'color': stat.get_color(),
    }
    return attributes


def get_att_tram(stat: Station, last_node: Station) -> dict:
    attributes = {
        'type': 'tram',
        'weight': float(haversine(last_node.get_location(), stat.get_location()))*(1/30),
        'dist': haversine(last_node.get_location(), stat.get_location()),
        'speed': 26/(3.6), 
        'line': stat.get_line()[0],
        'color': colors[stat.get_line()[0]]
    }
    return attributes


def get_att_node_access(access: Access) -> dict:
    attributes = {
        'type': 'Access',
        'pos': access.get_location(),
        'accessibility': access.get_acssesstype()
    }
    return attributes


def get_att_edge_access(access: Access, dist: float) -> dict:
    attributes = {
            'type': 'Access',
            'weight': dist*(1/6),
            'dist': dist, 
            'speed': 6/(3.6), 
            'line': 'Null',
            'color': 'black' 
        }
    return attributes


def get_att_link(stat1: str, stat2: str, dist: float) -> dict:
    attributes = {
        'type': 'Link',
        'weight': dist*(1/6),
        'dist': dist,
        'speed': 6/(3.6), 
        'line': 'Null',
        'color': 'black'  
        }
    return attributes


def get_node_station_name(stat: Station) -> str:
    return stat.get_name() + '-' + str(stat.get_station_code())


def get_node_access_name(access: Access) -> str:
    return access.get_name() + '/' + str(access.get_station_code())


def add_station_node(metro: MetroGraph(), stat: Station, dict_stations: dict) -> None:
    att: dict = get_att_station(stat)
    node: str = stat.get_name() + '-' + str(stat.get_station_code())
    metro.add_node(node, **att)
    key: str = stat.get_name()
    if key in dict_stations:
        dict_stations[key].append(node)
    else:
        dict_stations[key] = [node]


def add_tram_edge(metro: MetroGraph(), stat1: Station, stat2: Station) -> None:
    att = get_att_tram(stat1, stat2)
    metro.add_edge(get_node_station_name(stat1), get_node_station_name(stat2), **att)


def add_access_node(metro: MetroGraph, access: Access) -> None:
    att = get_att_node_access(access)
    metro.add_node(get_node_access_name(access), **att)


def add_access_edge(metro: MetroGraph, access: Access) -> None:
    s = access.get_station_name() + '-' + str(access.get_station_code())
    s1 = get_node_access_name(access)
    att = get_att_edge_access(access, haversine(metro.nodes[s]['pos'], metro.nodes[s1]['pos'])) #no hi ha weight
    metro.add_edge(s, s1, **att)


def add_link_edge(metro: MetroGraph, lst_station: list) -> None:
    for stat1 in lst_station:
        for stat2 in lst_station:
            if stat1 != stat2:
                dist = haversine(metro.nodes[stat1]['pos'], metro.nodes[stat2]['pos'])
                att = get_att_link(stat1, stat2, dist)
                metro.add_edge(stat1, stat2, **att)


def add_nodes_and_edges(metro: MetroGraph, lst_stations: Stations, lst_accesses: Accesses, dict_stations: dict) -> None:
    last_line: Optional[str] = None
    last_node: Optional[Station] = None

    for stat in lst_stations:
        add_station_node(metro, stat, dict_stations)
        if stat._line[0] != last_line:
            last_line = stat.get_line()[0]
        else:
            add_tram_edge(metro, stat, last_node)
        last_node = stat

    for access in lst_accesses: 
        add_access_node(metro, access)
        add_access_edge(metro, access)

    for key in dict_stations:
        add_link_edge(metro, dict_stations[key])


def get_metro_graph() -> MetroGraph:
    metro = MetroGraph()
    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()
    dict_stations: dict = {}
    add_nodes_and_edges(metro, lst_stations, lst_accesses, dict_stations)
    return metro


def show(g: MetroGraph) -> None:
    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, node_color="red", edge_color="blue", with_labels=False)
    plt.show()


colors : dict = {'Null': 'black', 'L1': 'red', 'L2': 'purple', 'L3': 'green', 'L4': 'yellow', 'L5': 'blue', 
                       'L6': 'violet', 'L7': 'brown', 'L8': 'pink', 'L9S': 'orange', 'L9N': 'orange',
                                'L10N': 'cyan', 'L10S': 'cyan', 'L11': 'lime', 'FM': 'white'}

def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(680, 600, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    for index, node in g.nodes(data=True):
        coord = (node['pos'])
        marker_node = CircleMarker(coord, 'white', 2)
        marker_outline = CircleMarker(coord, 'black', 4)
        m.add_marker(marker_outline)
        m.add_marker(marker_node)
    for n1 in g.edges(data=True):
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        color = g.edges[n1[0], n1[1]]['color']
        line = Line(coord, color, 5)
        m.add_line(line)
    image = m.render()
    image.save(filename, quality=100)


def exec() -> None:
    m = get_metro_graph()
    #show(m)
    plot(m, 'filename.png')

exec()