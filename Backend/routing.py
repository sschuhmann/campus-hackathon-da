import googlemaps
from datetime import datetime

class Routing:

    API_KEY = 'AIzaSyDojPJdOWXgxyFBoeXmZLRmZXfODygwnjY'

    def __init__():
        self.gmaps = googlemaps.Client(key=API_KEY)


    def get_route_car(self, start, destination):
        now = datetime.now()
        try:
            directions_result = self.gmaps.directions(start,
                destination,
                mode='driving',
                departure_time=now)
        except:
            logging.error()

        return directions_result


    def get_route_train(self, start, destination):
        try:
            direction_result = self.gmaps.directions(start,
                                    destination,
                                    mode='transit',
                                    departure_time=now)
        except:
            logging.error()

        return direction_result

    def get_route_bike(self, start, destination):
        direction_result = self.gmaps.directions()
