from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add-user', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(data)

if __name__ == "__main__":
    app.run()