import requests
from database_utils import retrieve_from_database_without_json
from pprint import pprint
from table_names import *

kQUERY_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key={}"
kAPI_KEY = "AIzaSyABkkdZcbLVgXidTnfII6QHDVi4MT_9Xmg"

def format_request_url(query_type, query_city):
    return kQUERY_URL.format(query_type, query_city, kAPI_KEY)

def get_restaurants(pricing, interest_set_id):
    cuisines = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "cuisines")

    for i in range (0, len(cuisines[0][0])):
        request_url = format_request_url(cuisines[0][0][i] + " restaurants", "Chicago")
        restaurant_data = requests.get(request_url).json()
        pprint(restaurant_data)

def get_attractions(pricing, interest_set_id):
    attractions = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "attractions")

    for i in range (0, len(attractions[0][0])):
        request_url = format_request_url(attractions[0][0][i] + " attractions", "Chicago")
        attractions_data = requests.get(request_url).json()
        pprint(attractions_data)

def generate_trip(data):
    get_restaurants(2, data["interest_set_id"])