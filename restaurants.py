import pandas as pd
from typing_extensions import TypeAlias
from typing import List, Tuple
from dataclasses import dataclass
from fuzzysearch import find_near_matches


location = Tuple[float, float]  # (latitude, longitude)


@dataclass
class Restaurant:

    _name: str  # restaurant's name
    _adress: Tuple[str, str]  # restaurant's street name and number
    _neighborhood: str  # restaurnat's neighborhood name
    _district: str  # restaurnat's district name
    _tel: str  # restaurant's phone number
    _info: str  # restaurant's type
    _coord: location  # resturant's location

    def get_name(self) -> str:
        return self._name

    def get_adress(self) -> Tuple[str, str]:
        return self._adress

    def get_neighborhood(self) -> str:
        return self._neighborhood

    def get_district(self) -> str:
        return self._district

    def get_tel(self) -> str:
        return self._tel

    def get_info(self) -> str:
        return self._info

    def get_coord(self) -> location:
        return self._coord


Restaurants: TypeAlias = List[Restaurant]


def read() -> Restaurants:
    """Reads and returns the list of restaurants
    Prec: the file 'restaurants.csv' must be downloanded"""

    df = pd.read_csv('restaurants.csv')
    # we pass the df readed into a str to get the correct format of the data
    df = df.astype(str)

    Rest_lst: Restaurants = []

    for index, row in df.iterrows():
        rest = Restaurant(row['name'], (row['addresses_road_name'], row['addresses_start_street_number'][:-2]),
                row['addresses_neighborhood_name'], row['addresses_district_name'], row['values_value'],
                row['secondary_filters_name'], (float(row['geo_epgs_4326_x']), float(row['geo_epgs_4326_y'])))
        Rest_lst.append(rest)

    return Rest_lst


def string_rest(rest: Restaurant) -> str:
    """Returns a string containing all the relevant information
    of the rest that might satisfy a query"""

    str_rest: str = ''
    str_rest += rest.get_name() + ' '
    str_rest += rest.get_adress()[0] + ' '
    str_rest += rest.get_neighborhood() + ' '
    str_rest += rest.get_district() + ' '
    str_rest += rest.get_info()
    return str_rest


def found(word_query: str, str_rest: str) -> bool:
    """Returns if the word_rest matches with a max_l_dist of 1
    any word of the str_rest
    Prec: the word_query and the str_rest must be a lower cases words"""

    for word_rest in str_rest.split():
        if find_near_matches(word_query, word_rest, max_l_dist=1) != []:
            return True
    return False


def coincidence(query: str, rest: Restaurant) -> bool:
    """Returns if the rest satisfies the query"""

    # we create a string with the relevant information of the rest concatenated
    str_rest: str = string_rest(rest)

    # we check if every word in the query matches with the rest
    for word_query in query.split():
        if not found(word_query.lower(), str_rest.lower()):
            return False
    return True


def find(query: str, restaurants: Restaurants) -> Restaurants:
    """Given a query and a list of restaurants returns a list of
    restaurants that satisfy the query"""

    restaurants_query: Restaurants = []

    for rest in restaurants:
        if coincidence(query, rest):
            restaurants_query.append(rest)

    return restaurants_query
