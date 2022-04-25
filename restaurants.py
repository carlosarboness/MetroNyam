from typing import Optional, List, Tuple


class Restaurant:

    _id: int
    _name: str
    _adress: Tuple[str, int]
    _neighbourhood: str
    _district: str
    _zip_code: int
    _tel: int

    def __init__(self, id: int, name: str, adress: Tuple[str, int], neighbourhood: str, district: str, zip_code: int, tel: int) -> None:
        _id = id
        _name = name
        _adress = adress
        _neighbourhood = neighbourhood
        _district = district
        _zip_code = zip_code
        _tel = tel


Restaurants = List[Restaurant]


def read() -> Restaurants:
    return


def coincidence(query: str, res: Restaurant) -> bool:
    return query.lower() == (str(res._id) or res._adress[0].lower() or res._neighbourhood.lower() or res._district.lower() or str(res._zip_code))


def find(query: str, restaurants: Restaurants) -> Restaurants:
    restaurants_query: Restaurants = []
    for restaurant in restaurants:
        if coincidence(query, restaurant):
            restaurants_query.append(restaurant)
    return restaurants_query
