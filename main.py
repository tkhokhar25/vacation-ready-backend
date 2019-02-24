from flask import Flask, request, jsonify
from add_user import *
from interest_sets import *
from trip_generator import generate_trip

app = Flask(__name__)

@app.route('/add-user', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        data = request.get_json()

        return jsonify(add_user_entry(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/update-user-details', methods=['GET', 'POST'])
def update_user_details():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(update_user_entry(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/set-interest-set', methods=['GET', 'POST'])
def set_interest_set():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(set_interest(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/get-interest-set', methods=['GET', 'POST'])
def get_interest_set():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(get_interest(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/update-interest-set', methods=['GET', 'POST'])
def update_interest_set():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(update_interest(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/generate-trip', methods=['GET', 'POST'])
def generate_trip_endpoint():
        if request.method == 'POST':
                data = request.get_json()
                generate_trip(data)

                return jsonify({"STATUS" : "SUCCESS"}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run()