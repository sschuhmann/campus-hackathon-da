from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify
import uuid
import datetime

import routing
from routing import Reasoning

import logging

value_map = {}

server = Flask(__name__)
CORS(server)

r = routing.Routing()
reasoner = Reasoning()

logging.getLogger().setLevel(logging.DEBUG)

"""
@server.route('/tour', methods=['POST'])
def get_tour():
    logging.debug("Getting tour request")
    content = request.json

    if not content:
        logging.debug("No json content")

        return jsonify({"Message": "No content"})
    try: 
        return jsonify({})
    except:
        return jsonify({"": ""})

""" 

@server.route('/route', methods=['POST'])
def get_route():
    logging.debug("Getting location request")
    content = request.json

    if not content:
        return "No data send"

    logging.debug(str(content))
    timestamp = None

    try: 
        if 'date_time' in content:
            timestamp = datetime.datetime.strptime(
                                    content['date_time'], 
                                    "%Y-%m-%dT%H:%M")

        feature_set = r.build_feature_set(content['start'], 
                            content['destination'], 
                            timestamp)

        res = reasoner.recommendation(feature_set)
        id = uuid.uuid4().hex
        value_map['id'] = feature_set 
        res['id'] = id
        return jsonify(res)
    except Exception as e:
        logging.error("Error: " + str(e))
        return jsonify({"Error": "No route"})

    else:
        return "Wrong dataset", 206

    return 

@server.route('/feedback', methods=["POST"])
def feedback():
    logging.info("Feedback called")
    timestamp = None

    content = request.json

    if not content:
        return "No data send"

    if 'id' in content:
        if not id in value_map:
            return jsonify({"Message": "Id not found"})

    if 'date_time' in content:
        timestamp = datetime.datetime.strptime(
                            content['date_time'], 
                            "%Y-%m-%dT%H:%M")
    
    feature_type = content['type']

    reasoner.train_model(value_map['id'], feature_type)

    return jsonify({"Message": "Model trained"}), 200

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=12000,debug=True)