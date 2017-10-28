from flask import Flask
import logging
from flask import request

from routing import route

server = Flask(__name__)

route = routing.Route()

@server.route('/route/')
def get_route():
    logging.info("Request")
    start = request.args.get('start')
    destination = requests.args.get('destination')
    time = requests.args.get('date_time')
    logging.info(str(content))
    route.get_route_car(content[start],
                content[destination])

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
