from flask import Flask, render_template, request
import json

from google.protobuf.json_format import MessageToJson

import service
from service import railroad_client as client

from secret import MAPS_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    cities = None
    with open('cities.json') as f:
        cities = json.loads(f.read())

    return render_template('map.html', cities=cities, api_key=MAPS_API_KEY)

@app.route('/allLines')
def get_all_lines():
    return MessageToJson(client.get_all_paths())

@app.route('/fetchSearchResults')
def perform_search():
    source = request.args.get('source', '')
    destination = request.args.get('destination', '')

    return MessageToJson(client.perform_search(source, destination))

if __name__ == '__main__':
    app.run()
