
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
    
    def get_district(self) -> str: 
        return self._district
    
    def get_tel(self) -> int: 
        return self._tel
        
Restaurants = List[Restaurant]

def read() -> Restaurants:
    #http://www.bcn.cat/tercerlloc/files/restaurants/opendatabcn_restaurants_restaurants-csv.csv
    df = pd.read_csv('rest.csv')
    Restaurants_list: List[Restaurant] = []
    for index, row in df.iterrows():
        r = Restaurant(row['register_id'], row['name'], (row['addresses_road_name'], row['addresses_start_street_number']), 
                        row['addresses_neighborhood_name'], row['addresses_district_name'], row['addresses_zip_code'], row['values_value'])
        Restaurants_list.append(r)
    return Restaurants_list
   
def coincidence(query: str, res: Restaurant) -> bool:
    return query.lower() == (str(res._id) or res._adress[0].lower() or res._neighbourhood.lower() or res._district.lower() or str(res._zip_code))

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
    query = "Eixample"
    filter = find(query, restaurants)
    print(len(filter))
    
exec()