import googlemaps
from datetime import datetime
import json
import logging
import pprint
import json

#import ml-model as ml

logging.getLogger().setLevel(logging.DEBUG)

class Routing:

    def __init__(self):
        self.API_KEY = 'AIzaSyDojPJdOWXgxyFBoeXmZLRmZXfODygwnjY'
        self.gmaps = googlemaps.Client(key=self.API_KEY)

    def get_route(self, start, destination, timestamp, mode):
        now = datetime.now()
        try:
            direction_result = self.gmaps.directions(start, 
                destination,
                mode=mode,
                units='metric',
                departure_time=now)

            for n in direction_result:
                if 'legs' in n:
                    return n['legs'][0]

                for l in n['legs']:
                    logging.debug(str(l['distance']))
                    logging.debug("Duration " + str(l['duration']))
                    logging.debug("Traffric " + str(l['duration_in_traffic']))

        except Exception as e:
            logging.error("Error getting data " + str(e))
            return None

    def get_route_car(self, start, destination, timestamp):
        result =  self.get_route(start, destination, timestamp, "driving")
        feature = []
        feature.append(result['duration']['value'])
        feature.append(result['distance']['value'])        
        return result  

    def get_route_bike(self, start, destination, timestamp):
        feature = []
        result =  self.get_route(start, destination, timestamp, "bicycling")
        feature.append(result['duration']['value'])
        feature.append(result['distance']['value'])
        logging.debug(feature)
        return result

    def get_route_transit(self, start, destination, timestamp):
        result = direction_result = self.gmaps.directions(start, destination, "transit")
        feature = []

        for n in result:
            for l in n['legs']:
                logging.debug("Train: " + str(l['duration']))
                feature.append(l['duration']['value'])
                feature.append(l['distance']['value'])
            
        
        logging.debug(feature)
        return feature
    
    def calc_best_time(self, start, destination, timestamp):
        res = {}
        feature = []

        feature.extend(self.get_route_car(start, destination, timestamp))
        feature.extend(self.get_route_bike(start, destination, timestamp))
        feature.extend(self.get_route_transit(start, destination, timestamp))

        # Add ml here

        logging.debug("Feature matrix: " + str(feature))






