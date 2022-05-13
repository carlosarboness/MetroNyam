from dataclasses import dataclass
from typing_extensions import TypeAlias
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


@dataclass
class Station:
    _station_code: str  # CODI_ESTACIO
    _name: str  # NOM_ESTACIO
    _line: str  # NOM_LINIA
    _color: str  # COLOR_LINIA
    _location: location  # GEOMETRY -with modifications-

    def get_station_code(self) -> str:
        return self._station_code

    def get_name(self) -> str:
        return self._name

    def get_line(self) -> str:
        return self._line

    def get_color(self) -> Tuple[str, int]:
        return self._color

    def get_location(self) -> location:
        return self._location


@dataclass
class Access:
    _name: str  # NOM_ACCES
    _station_code: str  # ID_ESTACIO
    _station_name: str  # NOM_ESTACIO
    _location: location  # GEOMETRY -with modifications-

    def get_name(self) -> str:
        return self._name

    def get_station_code(self) -> str:
        return self._station_code

    def get_station_name(self) -> str:
        return self._station_name

    def get_location(self) -> location:
        return self._location


Stations: TypeAlias = List[Station]


Accesses: TypeAlias = List[Access]


MetroGraph: TypeAlias = nx.Graph


def point(geomety: str) -> location:
    """Returns the location from a 'geometry' string
    Prec: geometry must be a string with the following format: 'POINT (longitud latitud)' """
    
    word_lst: list[str] = geomety.split()
    return (float(word_lst[1].replace('(', '')), float(word_lst[2].replace(')', '')))


def read_stations() -> Stations:
    """Reads and returns the list of stations
    Prec: the file 'estacions.csv' must be downloanded"""

    df = pd.read_csv('estacions.csv')
    df = df.astype(str)  # we pass the df readed into a strings to get the correct format of the data

    Stat_lst: Stations = []

    for index, row in df.iterrows():
        stat = Station(row['CODI_ESTACIO'], row['NOM_ESTACIO'], row['NOM_LINIA'],
                    row['COLOR_LINIA'], point(row['GEOMETRY']))
        Stat_lst.append(stat)

    return Stat_lst


def read_accesses() -> Accesses:
    """Reads and returns the list of accessess
    Prec: the file 'accessos.csv' must be downloanded"""

    df = pd.read_csv('accessos.csv')
    df = df.astype(str)  # we pass the df readed into a strings to get the correct format of the data

    Access_lst: Accesses = []

    for index, row in df.iterrows():
        access = Access(row['NOM_ACCES'], row['ID_ESTACIO'], row['NOM_ESTACIO'], point(row['GEOMETRY']))
        Access_lst.append(access)

    return Access_lst


def get_att_station(stat: Station) -> dict:
    """Retruns a map of the attrubutes of the node stat"""

    attributes: dict = {
        'type': 'Station',
        'name': stat.get_name(),
        'line': stat.get_line(),
        'pos': stat.get_location(),
        'color': stat.get_color(),
    }
    return attributes


def get_att_tram(stat1: Station, stat2: Station) -> dict:
    """Returns a map of the attributes of the edge between the stations stat1 and stat2"""

    attributes: dict = {
        'type': 'tram',
        'weight': float(haversine(stat2.get_location(), stat1.get_location()))*(1/30),
        'dist': haversine(stat2.get_location(), stat1.get_location()),
        'speed': 26/(3.6), 
        'line': stat1.get_line(),
        'color': get_colors()[stat1.get_line()]
    }
    return attributes


def get_att_node_access(access: Access) -> dict:
    """Returns a map of the attributes of the node access"""

    attributes: dict = {
        'type': 'Access',
        'pos': access.get_location()
    }
    return attributes


def get_att_edge_access(access: Access, dist: float) -> dict:
    """Returns a map of the attributes of the edge between an access
    and its station given the access and the distance to its station"""

    attributes: dict = {
            'type': 'Access',
            'weight': dist*(1/6),
            'dist': dist, 
            'speed': 6/(3.6), 
            'line': 'Null',
            'color': 'black'  # the color black means that it is walking
        }
    return attributes


def get_att_link(dist: float) -> dict:
    """Returns a map of the attributes of a link edge between two
    station given the distance between them"""

    attributes: dict = {
        'type': 'Link',
        'weight': dist*(1/6),
        'dist': dist,
        'speed': 6/(3.6), 
        'line': 'Null',
        'color': 'black'  # the color black means that it is walking
    }
    return attributes


def get_node_station_name(stat: Station) -> str:
    """Returns the name of the node access which consists of
    its name, '-' and its station code"""

    return stat.get_name() + '-' + stat.get_station_code()


def get_node_access_name(access: Access) -> str:
    """Returns the name of the node access which consists of
    its name, '/' and the station code that connects to it"""

    return access.get_name() + '/' + access.get_station_code()


def add_station_node(metro: MetroGraph, stat: Station, stat_map: dict) -> None:
    """Adds the node of the Station stat into the metro with its attrubites 
    and into the stat_map"""

    # add the node and its attributes to the metro
    att: dict = get_att_station(stat)
    node_name: str = get_node_station_name(stat)
    metro.add_node(node_name, **att)

    # add to the stat_map the node with the key being its name
    key: str = stat.get_name()
    if key in stat_map:
        stat_map[key].append(node_name)
    else:
        stat_map[key] = [node_name]


def add_tram_edge(metro: MetroGraph(), stat1: Station, stat2: Station) -> None:
    """Adds an edge into the metro between the node of the stations stat1 and stat2 with its attributes
    Prec: the nodes of the stat1 and stat2 must be in the metro"""

    att: dict = get_att_tram(stat1, stat2)
    metro.add_edge(get_node_station_name(stat1), get_node_station_name(stat2), **att)


def add_access_node(metro: MetroGraph, access: Access) -> None:
    """Adds the node of the access to the metro with its attributes"""

    att: dict = get_att_node_access(access)
    metro.add_node(get_node_access_name(access), **att)


def add_access_edge(metro: MetroGraph, access: Access) -> None:
    """Adds an edge in the metro between the access and its Station
    Prec: the nodes of the acces and its Station must be in the metro"""

    # we first build the station name that has to connect with the access and the access name
    stat_name = access.get_station_name() + '-' + access.get_station_code()
    access_name = get_node_access_name(access)

    # we get the attributes of the edge using the access and its distance to the node
    att: dict = get_att_edge_access(access, haversine(metro.nodes[stat_name]['pos'], metro.nodes[access_name]['pos']))

    metro.add_edge(stat_name, access_name, **att)


def add_link_edge(metro: MetroGraph, lst_station: list) -> None:
    """Given a list of stations, connects its nodes with link edges into the metro
    Prec: the nodes of the stations must be in the metro"""

    for stat1 in lst_station:
        for stat2 in lst_station:
            if stat1 != stat2:
                dist: float = haversine(metro.nodes[stat1]['pos'], metro.nodes[stat2]['pos'])
                att: dict = get_att_link(dist)
                metro.add_edge(stat1, stat2, **att)


def add_station_nodes_and_edges(metro_grf: MetroGraph, lst_stations: Stations, stat_map: dict) -> None:
    """Adds the station nodes to the metro_grf and the edges of the diferent metro lines and builds the
    stat_map storing the stations with the same name but diferent lines in the same key"""

    last_line: Optional[str] = None
    last_node: Optional[Station] = None

    # for every station in the list of station the station node is added and,
    # if they have the same line, an edge between them is also added
    for stat in lst_stations:
        add_station_node(metro_grf, stat, stat_map)
        if stat.get_line() == last_line:
            add_tram_edge(metro_grf, stat, last_node)
        else:
            last_line = stat.get_line()
        last_node = stat



def build_metro_graph(lst_stations: Stations, lst_accesses: Accesses) -> MetroGraph:
    """Given a list of stations and accesses returns its Metrograph"""

    metro_grf = MetroGraph()
    stat_map: dict = {}  # map that stores the stations with the same name but diferent lines in the same key

    add_station_nodes_and_edges(metro_grf, lst_stations, stat_map)

    for access in lst_accesses:
        add_access_node(metro_grf, access)
        add_access_edge(metro_grf, access)

    for key in stat_map:
        add_link_edge(metro_grf, stat_map[key])
    
    return metro_grf


def get_metro_graph() -> MetroGraph:
    """Returns the MetroGraph of the Barcelona metro"""

    lst_stations: Stations = read_stations()
    lst_accesses: Accesses = read_accesses()

    metro_grf: MetroGraph = build_metro_graph(lst_stations, lst_accesses)

    return metro_grf


def show(g: MetroGraph) -> None:
    """ Shows in an interactive screen the graph (nodes and edges) from g, that is the graph that contains 
    the graph of the metro of Barcelona """

    nx.draw(g, nx.get_node_attributes(g, 'pos'), node_size=10, node_color="red", edge_color="blue", with_labels=False)
    plt.show()


def get_colors() -> dict:
    """Returns a map of with de keys being the names of the lines and values being its colors"""

    colors : dict = {'Null': 'black', 'L1': 'red', 'L2': 'purple', 'L3': 'green', 
                    'L4': 'yellow', 'L5': 'blue', 'L6': 'violet', 'L7': 'brown',
                    'L8': 'pink', 'L9S': 'orange', 'L9N': 'orange', 'L10N': 'cyan', 
                    'L10S': 'cyan', 'L11': 'lime', 'FM': 'white'}
    return colors


def paint_nodes(g: MetroGraph, m: StaticMap) -> None:
    """ Paints all the nodes from the graph g in the StaticMap m with the color red """

    for index, node in g.nodes(data=True):
        coord = (node['pos'])
        marker_node = CircleMarker(coord, 'white', 2)
        m.add_marker(marker_node)


def paint_edges(g: MetroGraph, m: StaticMap) -> None:
    """ Paints all the edges from the graph g in the StaticMap m with the color blue """

    for n1 in g.edges(data=True):
        coord = (g.nodes[n1[0]]['pos'], g.nodes[n1[1]]['pos'])
        color = g.edges[n1[0], n1[1]]['color']
        line = Line(coord, color, 5)
        m.add_line(line)

def plot(g: MetroGraph, filename: str) -> None:
    """ Saves the image of the metrograph in the file -filename-. We iterate all the nodes, and  edges from the
    graph g and colour them with the image of the barcelona map at the background """

    url: str = 'http://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
    m: StaticMap = StaticMap(1000, 1000, url_template=url)

    paint_nodes(g, m)
    paint_edges(g, m)

    image = m.render()
    image.save(filename, quality=1000)
