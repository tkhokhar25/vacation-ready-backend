from flask import Flask, request, jsonify, render_template
from add_user import *
from interest_sets import *
from trip_generator import generate_trip
from trip_info import *
from place_reviews import *

import os       

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
        return render_template('index.html')

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

@app.route('/get-all-interest-sets', methods=['GET', 'POST'])
def get_all():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(get_all_interest_sets(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/delete-interest-set', methods=['GET', 'POST'])
def delete_interest():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(delete_interest_set(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/update-interest-set', methods=['GET', 'POST'])
def update_interest_set():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(update_interest(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/generate-trip', methods=['GET', 'POST'])
def generate_trip_endpoint():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(generate_trip(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/set-trip-info', methods=['GET', 'POST'])
def set_trip_set():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(set_trip_info(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/add-trip', methods=['GET', 'POST'])
def add_trip():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(create_trip(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/update-trip', methods=['GET', 'POST'])
def update_trip():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(modify_trip(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/delete-trip', methods=['GET', 'POST'])
def delete_trip():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(remove_trip(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/get-trip', methods=['GET', 'POST'])
def get_trip():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(fetch_trip(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/review-place', methods=['GET', 'POST'])
def review():
        if request.method == 'POST':
                data = request.get_json()

                return jsonify(review_place(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
        app.run()