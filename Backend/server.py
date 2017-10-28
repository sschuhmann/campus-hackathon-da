from flask import Flask
import logging
from flask import request

import routing

server = Flask(__name__)

route = routing.Route()

@server.route('/route/')
def get_route():
    logging.info("Request")
    content = request.json
    logging.info(str(content))
    route.get_route_car(content[start], content[destination])
    return "Hallo Welt"

@server.route('')
def store_user_settings():
    logging.info("Store settings")
    content = request.json
    logging.info(str(content))

    try:
        pass
    except:
        pass

if __name__ == '__main__':
    server.run(debug=True)
s
