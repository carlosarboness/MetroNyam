import pandas as pd
from staticmap import StaticMap, CircleMarker
from typing import Optional, List, Tuple

class Restaurant:

    _id: int #resigter_id
    _name: str #name
    _adress: Tuple[str, int] #[adress_road_name, adresses_strat_street_number]
    _neighborhood: str #adresses_neighborhood_name
    _district: str  #adresses_district_name
    _zip_code: int  #adresses_zip_code
    _tel: int   #values_value

    def __init__(self, id: int, name: str, adress: Tuple[str, int], neighborhood: str, district: str, zip_code: int, tel: int) -> None:

        self._id = id
        self._name = name
        self._adress = adress
        self._neighborhood = neighborhood
        self._district = district
        self._zip_code = zip_code
        self._tel = tel

    def get_name(self) -> str: 
        return self._name 
    
    def get_adress(self) -> Tuple[str, int]: 
        return self._adress
    
    def get_neighborhood(self) -> str:
        return self._neighborhood
    
    def get_district(self) -> str: 
        return self._district
    
    def get_zip_code(self) -> int: 
        return self._zip_code


Restaurants = List[Restaurant]

def read() -> Restaurants:
    #http://www.bcn.cat/tercerlloc/files/restaurants/opendatabcn_restaurants_restaurants-csv.csv
    df = pd.read_csv('rest.csv')
    df = df.astype(str) #we pass the df readed into a str
    Restaurants_list: List[Restaurant] = []
    for index, row in df.iterrows():
        r = Restaurant(row['register_id'], row['name'], (row['addresses_road_name'], row['addresses_start_street_number']), 
                        row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code'], row['values_value'])
        Restaurants_list.append(r)
    return Restaurants_list
   
def coincidence(query: str, res: Restaurant) -> bool:
    query = query.lower()
    lst_query: list[str] = []
    for w_query in query.split():
        lst_query.append(w_query)
    for w_query in lst_query:
        in_name: bool = False
        for w_name in res.get_name().split():
        #if res._name is a string with more than one word, we use de function split to
        #divide it into a list of strings (with only one word) to be able to compare it
            if w_query == w_name.lower():
                in_name = True
        adress: str = res.get_adress()[0].lower()
        neighborhood: str = res.get_neighborhood().lower()
        district: str = res.get_district().lower()
        zip_code: str = res.get_zip_code().lower()
        if not in_name and w_query != adress and w_query != neighborhood and w_query != district and w_query != zip_code:
            return False
    return True

def find(query: str, restaurants: Restaurants) -> Restaurants:
    restaurants_query: Restaurants = []
    for restaurant in restaurants:
        if coincidence(query, restaurant):
            restaurants_query.append(restaurant)
    return restaurants_query

def exec() -> None: 
    restaurants = read()
    for rest in restaurants: 
        print(rest._district)
    query = "Sushi"
    filter = find(query, restaurants)
    for rest in filter:
        print(rest._name, rest._neighborhood, rest._district)
    
exec()
