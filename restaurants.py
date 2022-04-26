import pandas as pd
from staticmap import StaticMap, CircleMarker
from typing import Optional, List, Tuple

class Restaurant:

    _id: str #resigter_id
    _name: str #name
    _adress: Tuple[str, str] #[adress_road_name, adresses_strat_street_number]
    _neighborhood: str #adresses_neighborhood_name
    _district: str  #adresses_district_name
    _zip_code: str  #adresses_zip_code
    _tel: str   #values_value

    def __init__(self, id: str, name: str, adress: Tuple[str, str], neighborhood: str, district: str, zip_code: str, tel: str) -> None:

        self._id = id
        self._name = name
        self._adress = adress
        self._neighborhood = neighborhood
        self._district = district
        self._zip_code = zip_code
        self._tel = tel

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
    for word in res.get_name().split():
    #if res._name is a string with more than one word, we use de function split to
    #divide it into a list of strings (with only one word) to be able to compare it
        if query == word.lower():
            return True
    adress: str = res.get_adress()[0].lower()
    neighborhood: str = res.get_neighborhood().lower()
    district: str = res.get_district().lower()
    zip_code: str = res.get_zip_code().lower()
    return query == adress or query == neighborhood or query == district or query == zip_code
    #ERRORS A CORREGIR:
    # - No funciona amb el zip_code 
    # - adress, neighborhood, district... també poden tenir més d'una paraula (fer com la mateixa funció de word)

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
    print()
    query = "C Olzinelles"
    filter = find(query, restaurants)
    for rest in filter:
        print(rest._name, rest._neighborhood, rest._district)
    
exec()
