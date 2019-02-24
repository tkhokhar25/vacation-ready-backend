import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import jsonify

kDATABASE_NAME = 'vacationready'
kUSER = 'tushar'
kPASSWORD = 'password'

def insert_format(table_name, keys, values):
    return "INSERT INTO {} {} VALUES {};".format(table_name, keys, values)

def get_database_connection():
    connection = psycopg2.connect(dbname = kDATABASE_NAME, user = kUSER, password = kPASSWORD, host = 'localhost')
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

def insert_into_database(table_name, json_data):
    keys, values = get_keys_and_values(json_data)

    connection = get_database_connection()
    cur = connection.cursor()

    try:
        cur.execute(insert_format(table_name, keys, values))
        
        return {"STATUS" : "SUCCESS"}
    except:

        return {"STATUS" : "FAILURE"}