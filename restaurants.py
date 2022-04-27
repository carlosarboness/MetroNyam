import pandas as pd
from staticmap import StaticMap, CircleMarker
from typing import Optional, List, Tuple
from fuzzysearch import find_near_matches


location = Tuple[str, str]


class Restaurant:

    _id: str  # resigter_id
    _name: str  # name
    _adress: Tuple[str, str]  # [adress_road_name, adresses_strat_street_number]
    _neighborhood: str  # adresses_neighborhood_name
    _district: str  # adresses_district_name
    _zip_code: str  # adresses_zip_code
    _tel: str  # values_value
    _coord: location  # [geo_epgs_4326_x, geo_epgs_4326_y]

    def __init__(self, id: str, name: str, adress: Tuple[str, str], neighborhood: str, district: str, zip_code: str, tel: str, coord: location) -> None:

        self._id = id
        self._name = name
        self._adress = adress
        self._neighborhood = neighborhood
        self._district = district
        self._zip_code = zip_code
        self._tel = tel
        self._coord = coord

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_adress(self) -> Tuple[str, str]:
        return self._adress

    def get_neighborhood(self) -> str:
        return self._neighborhood

    def get_district(self) -> str:
        return self._district

    def get_zip_code(self) -> str:
        return self._zip_code

    def get_tel(self) -> str:
        return self._tel

    def get_coord(self) -> location:
        return self._coord


Restaurants = List[Restaurant]


def read() -> Restaurants:
    # url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv'
    df = pd.read_csv('rest.csv')
    df = df.astype(str)  # we pass the df readed into a str
    Restaurants_list: List[Restaurant] = []
    for index, row in df.iterrows():
        r = Restaurant(row['register_id'], row['name'], (row['addresses_road_name'], row['addresses_start_street_number']),
                        row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code'], row['values_value'],
                        (row['geo_epgs_4326_x'], row['geo_epgs_4326_y']))
        Restaurants_list.append(r)
    return Restaurants_list


def split_compare_string(query: str, string: str) -> Optional[bool]:
    # if res._name is a string with more than one word, we use de function split to
    # divide it into a list of strings (with only one word) to be able to compare it
    for word in string.split():
        if query == word:
            return True
    return None


def lst_rest(rest: Restaurant) -> List[str]:
    lst: List[str] = []
    lst.append(rest.get_name().lower())
    lst.append(rest.get_adress()[0].lower())
    lst.append(rest.get_neighborhood().lower())
    lst.append(rest.get_district().lower())
    lst.append(rest.get_zip_code().lower())
    return lst


def coincidence(query: str, rest: Restaurant) -> bool:
    lst: List[str] = lst_rest(rest)
    for string in lst:
        if split_compare_string(query.lower(), string):
            return True
    return False
    # ERRORS A CORREGIR:
    # - No funciona amb el zip_code(8013.0)


def find(query: str, restaurants: Restaurants) -> Restaurants:
    restaurants_query: Restaurants = []
    for restaurant in restaurants:
        if coincidence(query, restaurant):
            restaurants_query.append(restaurant)
    return restaurants_query


def exec() -> None:
    restaurants = read()
    for rest in restaurants:
        print(rest._zip_code)
    print()
    query = "8013.0"
    filter = find(query, restaurants)
    for rest in filter:
        print(rest._name, rest._coord)

exec()
