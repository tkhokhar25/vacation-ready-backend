from database_utils import insert_into_database
from flask import jsonify
from table_names import *

def set_interest(json_data):
    return insert_into_database(kINTEREST_SET_TABLE, json_data)