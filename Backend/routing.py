import googlemaps
from datetime import datetime


class Routing:
    API_KEY = 'AIzaSyDojPJdOWXgxyFBoeXmZLRmZXfODygwnjY '

    def __init__():
        self.gmaps = googlemaps.Client(key=API_KEY)


    def get_route_car(self, start, destination):
        now = datetime.now()
        directions_result = self.gmaps.directions('Saarbruecken',
                                'Zweibruecken',
                                mode='car',
                                departure_time=now)
        return directions_result


    def get_route_train(self, start, destination):
        direction_result = self.gmaps.directions('Saarbruecken',
                                'Zweibrücken',
                                mode='train',
                                departure_time=now)

        return direction_result
