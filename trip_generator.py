import requests
from database_utils import retrieve_from_database_without_json
from pprint import pprint
from table_names import *

kRESTAURANT_QUERY_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key={}&minprice={}&maxprice={}"
kATTRACTION_QUERY_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key={}"
kPLACE_NAME_QUERY_URL = "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&fields=formatted_address&key={}"
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
    restaurant_json_formatted_entry['place_id'] = restaurant_entry['place_id']
    restaurant_json_formatted_entry['price_level'] = restaurant_entry['price_level']
    restaurant_json_formatted_entry['name'] = restaurant_entry['name']
    restaurant_json_formatted_entry['cuisine'] = cuisine
    restaurant_maps_link = restaurant_entry['photos'][0]['html_attributions'][0].split('"')[1].split('"')[0]
    restaurant_json_formatted_entry['maps_link'] = restaurant_maps_link
    restaurant_json_formatted_entry['lat'] = restaurant_entry['geometry']['location']['lat']
    restaurant_json_formatted_entry['lng'] = restaurant_entry['geometry']['location']['lng']
    
    return restaurant_json_formatted_entry

def filter_restaurants(restaurant_data, cuisine, all_restaurants_set):
    resturant_list = []

    for restaurant in restaurant_data['results']:
        resturant_entry = create_json_entry_for_restaurant(restaurant, cuisine)

        if resturant_entry['place_id'] not in all_restaurants_set:
            resturant_list.append(resturant_entry)
            all_restaurants_set.add(resturant_entry['place_id'])
    
    return resturant_list

def create_json_entry_for_attraction(attraction_entry):
    attraction_json_formatted_entry = {}
    attraction_json_formatted_entry['place_id'] = attraction_entry['place_id']
    attraction_json_formatted_entry['name'] = attraction_entry['name']
    attraction_json_formatted_entry['lat'] = attraction_entry['geometry']['location']['lat']
    attraction_json_formatted_entry['lng'] = attraction_entry['geometry']['location']['lng']
    try:
        attraction_maps_link = attraction_entry['photos'][0]['html_attributions'][0].split('"')[1].split('"')[0]
        attraction_json_formatted_entry['maps_link'] = attraction_maps_link
    except:
        attraction_json_formatted_entry['maps_link'] = None

    return attraction_json_formatted_entry

def filter_attractions(attractions_data, all_attractions_set):
    attractions_list = []

    for attraction in attractions_data['results']:
        attraction_entry = create_json_entry_for_attraction(attraction)

        if attraction_entry['place_id'] not in all_attractions_set:
            attractions_list.append(attraction_entry)
            all_attractions_set.add(attraction_entry['place_id'])

    return attractions_list

def format_restaurant_request_url(query_type, query_city, min_price, max_price):
    return kRESTAURANT_QUERY_URL.format(query_type, query_city, kAPI_KEY, min_price, max_price)

def format_attraction_request_url(query_type, query_city):
    return kATTRACTION_QUERY_URL.format(query_type, query_city, kAPI_KEY)

def format_place_name_query_url(place_id):
    return kPLACE_NAME_QUERY_URL.format(place_id, kAPI_KEY)

def get_place_name_from_id(place_id):
    request_url = format_place_name_query_url(place_id)
    place_name = requests.get(request_url).json()['result']['formatted_address']

    return place_name

def get_restaurants(interest_set_id):
    cuisines = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "cuisines")

    meal_budget = retrieve_from_database_without_json(kTRIP_INFO_TABLE, interest_set_id, "budget_per_meal")[0][0]
    place_id = retrieve_from_database_without_json(kTRIP_INFO_TABLE, interest_set_id, "place_id")[0][0]
    place_name = get_place_name_from_id(place_id)

    price_level = get_price_level(meal_budget)

    meal_times = ["breakfast", "lunch", "dinner"]
    suggested_restaurants = {meal_times[0] : [], meal_times[1] : [], meal_times[2] : []}

    all_restaurants_set = set()

    for i in range (0, len(meal_times)):
        for j in range (0, len(cuisines[0][0])):
            request_url = format_restaurant_request_url(cuisines[0][0][j] + " " + meal_times[i] + " restaurants", place_name, price_level - 1, price_level)
            restaurant_data = requests.get(request_url).json()
            if i == 2:
                pprint(restaurant_data)
            suggested_restaurants[meal_times[i]] += (filter_restaurants(restaurant_data, cuisines[0][0][j], all_restaurants_set))

    return suggested_restaurants

def get_attractions(interest_set_id):
    attractions = retrieve_from_database_without_json(kINTEREST_SET_TABLE, interest_set_id, "attractions")
    place_id = retrieve_from_database_without_json(kTRIP_INFO_TABLE, interest_set_id, "place_id")[0][0]
    place_name = get_place_name_from_id(place_id)

    suggested_attractions = {}

    all_attractions_set = set()

    for i in range (0, len(attractions[0][0])):
        request_url = format_attraction_request_url(attractions[0][0][i] + " attractions", place_name)
        attractions_data = requests.get(request_url).json()

        suggested_attractions[attractions[0][0][i]] = (filter_attractions(attractions_data, all_attractions_set))

    return suggested_attractions

def generate_trip(data):
    trip_places = {}

    trip_places["restaurants"] = get_restaurants(data["interest_set_id"])
    trip_places["attractions"] = get_attractions(data["interest_set_id"])

    return trip_places