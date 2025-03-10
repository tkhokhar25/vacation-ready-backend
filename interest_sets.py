from database_utils import insert_into_database, retrieve_from_database, update_in_database, delete_from_database
from flask import jsonify
from table_names import *

def set_interest(json_data):
    return insert_into_database(kINTEREST_SET_TABLE, json_data, "interest_set_id")

def get_interest(json_data):
    return retrieve_from_database("*", kINTEREST_SET_TABLE, "interest_set_id", json_data["interest_set_id"])

def update_interest(json_data):
        interest_set_id = json_data["interest_set_id"]

        return update_in_database(kINTEREST_SET_TABLE, json_data, "interest_set_id", interest_set_id)

def get_all_interest_sets(json_data):
    return retrieve_from_database("*", kINTEREST_SET_TABLE, "user_id", json_data["user_id"])

def delete_interest_set(json_data):
    return delete_from_database(kINTEREST_SET_TABLE, "interest_set_id", json_data["interest_set_id"])