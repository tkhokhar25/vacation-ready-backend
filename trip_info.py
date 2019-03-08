from database_utils import insert_into_database, retrieve_from_database, update_in_database
from flask import jsonify
from table_names import *

def set_trip_info(json_data):
    return insert_into_database(kTRIP_INFO_TABLE, json_data, "trip_id")