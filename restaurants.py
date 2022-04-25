@dataclass 
class Restaurant: ...

Restaurants = List[Restaurant]


def read() -> Restaurants: ...


def find(query: str, restaurants: Restaurants) -> Restaurants: ...