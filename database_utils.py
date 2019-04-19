import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import jsonify
import json
from pprint import pprint

kDATABASE_NAME = 'dbqvqb417h75ok'
kUSER = 'syellmnssqszzw'
kPASSWORD = 'fc2a87a6d11f20b99463426f94d11aa60b21817f803402c2e70ca5904403d6ab'
kHOST = 'ec2-50-17-193-83.compute-1.amazonaws.com'

def display_data_as_json(cur, result):
    response = '{ "result": ['

    for j in range (0, len(result)):

        response += '{'

        for i in range (0, len(result[j])):
            value = result[j][i]
            
            if (type(value) != int and type(value) != list):
                value = '"' + str(value) + '"'          
            elif (type(value) == list):
                value = json.dumps(value)

            response += ('"' + str(cur.description[i][0]) + '" : ' + str(value))
            response += ','

        response = response[:-1] + '},'

    response = response[:-1] + ']}'

    return json.loads(response)

def insert_format(table_name, keys, values, to_return):
    return "INSERT INTO {} {} VALUES {} RETURNING {}".format(table_name, keys, values, to_return)

def retrieve_format(to_select, table_name, key, value):
    return "SELECT {} FROM {} WHERE {} = {}".format(to_select, table_name, key, value)

def update_format(table_name, keys, values, entry_id_name, entry_id_value):
    return "UPDATE {} SET {} = {} WHERE {} = {}".format(table_name, keys, values, entry_id_name, entry_id_value)

def delete_format(table_name, key, value):
    return "DELETE FROM {} WHERE {} = {}".format(table_name, key, value)

def get_database_connection():
    connection = psycopg2.connect(dbname = kDATABASE_NAME, user = kUSER, password = kPASSWORD, host = kHOST)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return connection

def get_keys_and_values(data):
    keys = '('
    values = '('

    for key in data:
        keys += key
        keys += ', '
        
        if (type(data[key]) == list):
            values += "'[" + (",".join(map(str, data[key]))) + "]'"
        else:
            values += "'" + str(data[key]) + "'"
        
        values += ', '

    keys = keys[:-2] + ')'
    values = (values[:-2] + ')').replace('[', '{').replace(']', '}')

    return keys, values

def insert_into_database(table_name, json_data, to_return):
    keys, values = get_keys_and_values(json_data)

    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(insert_format(table_name, keys, values, to_return))

        return {"STATUS" : "SUCCESS", to_return : cur.fetchall()[0][0]}
    except:

        return {"STATUS" : "FAILURE"}

def retrieve_from_database(to_retrieve, table_name, key, value):
    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(retrieve_format(to_retrieve, table_name, key, value))
        
        return display_data_as_json(cur, cur.fetchall())
    except:

        return {"STATUS" : "FAILURE"}

def update_in_database(table_name, json_data, entry_id_name, entry_id_value):
    keys, values = get_keys_and_values(json_data)

    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(update_format(table_name, keys, values, entry_id_name, entry_id_value))

        return {"STATUS" : "SUCCESS"}
    except:

        return {"STATUS" : "FAILURE"}

def delete_from_database(table_name, key, value):
    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(delete_format(table_name, key, value))
        
        return {"STATUS" : "FAILURE"}
    except:

        return {"STATUS" : "FAILURE"}

def retrieve_from_database_without_json(table_name, interest_set_id, value):
    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(retrieve_format(table_name, interest_set_id, value))
        
        return cur.fetchall()
    except:

        return -1