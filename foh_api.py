import json

from flask import Flask, jsonify, request
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "Data","Server Memory", "latest_show.json")

@app.route('/channel_list',methods=['GET'])

def get_channel_list():
    if not os.path.isfile(DATA_FILE):
        return jsonify({"inputs": [], "outputs": []})
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/update_channel_list', methods=['POST'])

def update_channel_list():
    updated_list = request.json  # extract JSON data
    if updated_list:
       with open(DATA_FILE, "w") as f:
           json.dump(updated_list, f, indent=4)
       return jsonify({"status": "success", "message": "Channel list updated"}), 200
    else:
       return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
