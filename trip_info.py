from database_utils import insert_into_database, retrieve_from_database, update_in_database, delete_from_database
from flask import jsonify
from table_names import *

def set_trip_info(json_data):
    return insert_into_database(kTRIP_INFO_TABLE, json_data, "trip_id")

def parse_json_to_insert(json_data, index):
    insert_format = {}
    insert_format['trip_id'] = json_data['trip_id']
    insert_format['day_num'] = json_data['day_num']
    insert_format['lat'] = json_data['day_details'][index]['lat']
    insert_format['lng'] = json_data['day_details'][index]['lng']
    insert_format['maps_link'] = json_data['day_details'][index]['maps_link']
    insert_format['name'] = json_data['day_details'][index]['name']
    insert_format['place_id'] = json_data['day_details'][index]['place_id']
    
    return insert_format

def create_trip(json_data):
    for i in range(0, len(json_data['day_details'])):
        insert_format = parse_json_to_insert(json_data, i)
        insert_into_database(KTRIP_TABLE, insert_format, 'trip_id')
    
    return {'STATUS' : 'SUCCESS'}

def modify_trip(json_data):
    remove_trip({"trip_id" : json_data['trip_id']})
    create_trip(json_data)
    
    return {'STATUS' : 'SUCCESS'}
    
def remove_trip(json_data):
    return delete_from_database(KTRIP_TABLE, "trip_id", json_data["trip_id"])

def fetch_trip(json_data):
    to_update = '(' + str(json_data['trip_id']) + ', ' + str(json_data['day_num']) + ')'
    to_retrieve = 'place_id, lat, lng, maps_link, name'

    return retrieve_from_database(to_retrieve, KTRIP_TABLE, "(trip_id, day_num)", to_update)