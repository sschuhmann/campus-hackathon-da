from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import routing

import logging


server = Flask(__name__)
CORS(server)

r = routing.Routing()
logging.getLogger().setLevel(logging.DEBUG)

@server.route('/route', methods=['POST'])
def get_route():
    logging.debug("Getting location request")
    content = request.json

    if not content:
        return "No data send"

    logging.error(str(content))

    if True:
        r.calc_best_time(content['start'], content['destination'], "")
        return jsonify('{"recommendation": "car"}')
    else:
        return "Wrong dataset"

    return "Hallo Welt"

@server.route('/feedback', methods=["POST"])
def feedback():
    logging.info("Test")
    return "OK"

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=12000,debug=True)
