from database_utils import insert_into_database, update_in_database
from flask import jsonify
from table_names import *

def add_user_entry(json_data):
    return insert_into_database(kPEOPLE_TABLE, json_data, "user_id")

def update_user_entry(json_data):
    user_id = json_data["user_id"]

    return update_in_database(kPEOPLE_TABLE, json_data, "user_id", user_id)