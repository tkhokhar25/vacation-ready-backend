from flask import Flask, request, jsonify
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

                return jsonify(set_interest(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run()