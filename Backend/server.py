from flask import Flask
import logging
from flask import request

import routing  
server = Flask(__name__)
route = routing.Route

@server.route('/route/')
def get_route():
    logging.info("Request")
    content = request.json
    logging.info(str(content))
    return "Hallo Welt"



if __name__ == '__main__':
    server.run(debug=True)
