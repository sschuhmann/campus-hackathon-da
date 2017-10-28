from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import routing
from routing import Reasoning

import logging


server = Flask(__name__)
CORS(server)

r = routing.Routing()
reasoner = Reasoning()

logging.getLogger().setLevel(logging.DEBUG)

@server.route('/route', methods=['POST'])
def get_route():
    logging.debug("Getting location request")
    content = request.json

    if not content:
        return "No data send"

    logging.debug(str(content))

    if True:
        feature_set = r.build_feature_set(content['start'], content['destination'], "")
        res = reasoner.recommendation(feature_set)
        return jsonify(res), 200
    else:
        return "Wrong dataset", 206

    return 

@server.route('/feedback', methods=["POST"])
def feedback():
    logging.info("Feedback called")

    content = request.json

    if not content:
        return "No data send"

    logging.debug(str(content))

    feature_set = r.build_feature_set(content['start'], content['destination'], "")
    feature_type = content['type']

    reasoner.train_model(feature_set, feature_type)

    return "Ok", 200

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=12000,debug=True)
