from connect_to_database import get_database_connection
from flask import jsonify

def set_interest(json_data):
    connection = get_database_connection()
    cur = connection.cursor()
    
    try:
        temp = json_data['first']
        cur.execute("INSERT INTO interest_set (first) VALUES ('{}');", temp)
        return jsonify("STATUS : SUCCESS")
    except:
        return jsonify("STATUS: FAILURE")