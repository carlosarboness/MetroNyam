CityGraph = networkx.Graph

def get_osmnx_graph() -> OsmnxGraph: ... 

OsmnxGraph = networkx.MultiDiGraph

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None: ... 
    # guarda el graf g al fitxer filename
def load_osmnx_graph(filename: str) -> OsmnxGraph: ... 
    # retorna el graf guardat al fitxer filename

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: ... 
# retorna un graf fusió de g1 i g2

Coord = (float, float)   # (latitude, longitude)

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> 
Path: ...

NodeID = Union[int, str]
Path = List[NodeID]

def show(g: CityGraph) -> None: ... 
    # mostra g de forma interactiva en una finestra
def plot(g: CityGraph, filename: str) -> None: ... 
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ... 
    # mostra el camí p en l'arxiu filename