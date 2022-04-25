
import string


class Restaurant:

    _id : int
    _name : string
    _adress: string
    _neighbourhood: string
    _tel : int                 

    def __init__(self, id: int, name: string, adress: string, neighbourhood: string, tel: int) -> None:
        _id = id
        _name = name
        _adress = adress
        _neighbourhood = neighbourhood
        _tel = tel

Restaurants = list[Restaurant]


def read() -> Restaurants: 
    return 

def find(query: str, restaurants: Restaurants) -> Restaurants: 
    return