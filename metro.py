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
        'weight': haversine(last_node.get_location(), stat.get_location()),
        'line': stat.get_line()[0],
        'color': stat.get_color()
    }
    return attributes


def get_att_node_access(stat: Station, access: Access) -> dict:
    attributes = {
        'type': 'Access',
        'weight': haversine(stat.get_location(), access.get_location()),
        'pos': access.get_location(),
        'color': stat.get_color(),
        'accessibility': access.get_acssesstype()
    }
    return attributes


def get_att_edge_access(access: Access) -> dict:
    attributes = {
            'type': 'Access',
            'color': '005A97'  # color blanc
        }
    return attributes


def add_nodes_and_edges_from_lines(metro: MetroGraph(), lst_stations: Stations, lst_accesses: Accesses) -> None:
    last_line: Optional[str] = None
    last_node: Optional[Station] = None
    for stat in lst_stations:
        att = get_att_station(stat)
        metro.add_node(stat.get_name() + '-' + str(stat.get_station_code()), **att)
        if stat._line[0] != last_line:
            last_line = stat.get_line()[0]
        else:
            att = get_att_tram(stat, last_node)
            metro.add_edge(last_node.get_name() + '-' + str(last_node.get_station_code()), stat.get_name() + '-' + str(stat.get_station_code()), **att)
        last_node = stat
    for access in lst_accesses: 
        att = get_att_node_access(stat, access)
        metro.add_node(access.get_name() + '/' + str(access.get_station_code()), **att)
        att = get_att_edge_access(access) #no hi ha weight
        metro.add_edge((access.get_station_name() + '-' + str(access.get_station_code())), (access.get_name()) + '/' + str(access.get_station_code()), **att)


def get_att_link(stat1: Station, stat2: Station) -> dict:
    attributes = {
        'type': 'Link',
        'weight': haversine(stat1[1]['pos'], stat2[1]['pos']),
        'color': '005A97'  # color blanc
        }
    return attributes


def add_link_edges(metro: MetroGraph) -> None:
    for stat1 in metro.nodes(data=True):
        if stat1[1]['type'] == 'Station':
            for stat2 in metro.nodes(data=True):
                if stat2[1]['type'] == 'Station' and stat1 != stat2 and stat1[1]['name'] == stat2[1]['name']:
                        att = get_att_link(stat1, stat2)
                        metro.add_edge(stat1[0], stat2[0], **att)


def get_metro_graph() -> MetroGraph:
    metro = MetroGraph()
    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()
    add_nodes_and_edges_from_lines(metro, lst_stations, lst_accesses)
    add_link_edges(metro)
    return metro


def show(g: MetroGraph) -> None:
    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, node_color="red", edge_color="blue", with_labels=False)
    plt.show()


def plot(g: MetroGraph, filename: str) -> None:
    m = StaticMap(680, 600, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    for index, node in g.nodes(data=True):
        coord = (node['pos'])
        marker_node = CircleMarker(coord, 'red', 5)
        m.add_marker(marker_node)
    for n1 in g.edges(data=True):
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        line = Line(coord, 'blue', 2)
        m.add_line(line)
    image = m.render()
    image.save(filename, quality=100)


def exec() -> None:
    m = get_metro_graph()
    for node in m.nodes.data():
        print(node)
    print()
    for edge in m.edges.data():
        print(edge)
    show(m)
    plot(m, 'filename.png')