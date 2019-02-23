from flask import Flask, request, jsonify
from connect_to_database import get_database_connection
from interest_sets import *

app = Flask(__name__)

@app.route('/add-user', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(data)

@app.route('/set-interest-set', methods=['GET', 'POST'])
def set_interest_set():
        if request.method == 'POST':
                data = request.get_json()
                return set_interest(data)

if __name__ == "__main__":
    app.run()