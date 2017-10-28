from flask import Flask
import logging
from flask import request

server = Flask(__name__)

@server.route('/route/')
def get_route():
    logging.info("Request")
    start = request.json
    logging.info(str(content))

    return "Hallo Welt"

@server.route('/')
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
