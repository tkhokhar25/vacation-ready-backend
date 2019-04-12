import requests
from database_utils import retrieve_from_database_without_json
from pprint import pprint
from table_names import *

kRESTAURANT_QUERY_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key={}&minprice={}&maxprice={}"
kATTRACTION_QUERY_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key={}"
kAPI_KEY = "AIzaSyABkkdZcbLVgXidTnfII6QHDVi4MT_9Xmg"

def get_price_level(meal_budget):
    if meal_budget <= 15:
        return 1
    elif meal_budget <= 25:
        return 2
    elif meal_budget <= 45:
        return 3
    else:
        return 4

def create_json_entry_for_restaurant(restaurant_entry, cuisine):
    restaurant_json_formatted_entry = {}
    restaurant_id = restaurant_entry['place_id']
    restaurant_json_formatted_entry[restaurant_id] = {}
    restaurant_json_formatted_entry[restaurant_id]['price_level'] = restaurant_entry['price_level']
    restaurant_json_formatted_entry[restaurant_id]['price_level'] = restaurant_entry['price_level']
    restaurant_json_formatted_entry[restaurant_id]['name'] = restaurant_entry['name']
    restaurant_json_formatted_entry[restaurant_id]['cuisine'] = cuisine
    restaurant_maps_link = restaurant_entry['photos'][0]['html_attributions'][0].split('"')[1].split('"')[0]
    restaurant_json_formatted_entry[restaurant_id]['maps_link'] = restaurant_maps_link
    
    return restaurant_json_formatted_entry

def filter_restaurants(restaurant_data, cuisine):
    # pprint(restaurant_data)
    id_to_rating = {}
    resturant_list = []

    for restaurant in restaurant_data['results']:
        id_to_rating[restaurant['place_id']] = restaurant['rating']
        resturant_list.append(create_json_entry_for_restaurant(restaurant, cuisine))
    
    return resturant_list

def filter_attractions(attractions_data):
    id_to_rating = {}

    for attraction in attractions_data['results']:
        id_to_rating[attraction['place_id']] = attraction['rating']

    return sorted(id_to_rating.items(), key=lambda x: x[1])

def format_restaurant_request_url(query_type, query_city, min_price, max_price):
    return kRESTAURANT_QUERY_URL.format(query_type, query_city, kAPI_KEY, min_price, max_price)

def format_attraction_request_url(query_type, query_city):
    return kATTRACTION_QUERY_URL.format(query_type, query_city, kAPI_KEY)

def get_restaurants(pricing, interest_set_id):
    cuisines = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "cuisines")
    meal_budget = retrieve_from_database_without_json(kTRIP_INFO_TABLE, interest_set_id, "budget_per_meal")[0][0]
    price_level = get_price_level(meal_budget)

    meal_times = ["breakfast", "lunch", "dinner"]
    suggested_restaurants = {meal_times[0] : [], meal_times[1] : [], meal_times[2] : []}

    for i in range (0, len(meal_times)):
        for j in range (0, len(cuisines[0][0])):
            request_url = format_restaurant_request_url(cuisines[0][0][j] + " " + meal_times[i] + " restaurants", "Chicago", price_level - 1, price_level)
            restaurant_data = requests.get(request_url).json()
            suggested_restaurants[meal_times[i]] += (filter_restaurants(restaurant_data, cuisines[0][0][j]))

    return suggested_restaurants

def get_attractions(pricing, interest_set_id):
    attractions = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "attractions")

    suggested_attractions = []

    for i in range (0, len(attractions[0][0])):
        request_url = format_attraction_request_url(attractions[0][0][i] + " attractions", "Chicago")
        attractions_data = requests.get(request_url).json()
        suggested_attractions.append(filter_attractions(attractions_data))

    return suggested_attractions

def generate_trip(data):
    return get_restaurants(2, data["interest_set_id"])