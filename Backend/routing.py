import googlemaps
from datetime import datetime
import json
import logging
import pprint
import json
from random import randint
import sys

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
        feature = []
        result =  self.get_route(start, destination, timestamp, "driving")

        if not result:
            return None

        try:
            feature.append(result['duration']['value'])
            feature.append(result['distance']['value']) 
            logging.debug("Feature set car: " + str(feature))       
            return feature 
        except:
            feature.append(sys.maxint, sys.maxint)
            return feature

         

    def get_route_bike(self, start, destination, timestamp):
        feature = []
        result =  self.get_route(start, destination, timestamp, "bicycling")

        if not result:
            return None

        try: 
            feature.append(result['duration']['value'])
            feature.append(result['distance']['value'])
            logging.debug("Feature set bike: " + str(feature))
        except:
            logging.error("Error getting bike route")
            feature.append(sys.maxint, sys.maxint)

        return feature        

    def get_route_transit(self, start, destination, timestamp):
        result = direction_result = self.gmaps.directions(start, destination, "transit")
        feature = []

        if not result:
            return None

        try:
            for n in result:
                for l in n['legs']:
                    logging.debug("Train: " + str(l['duration']))
                    feature.append(l['duration']['value'])
                    feature.append(l['distance']['value'])
        except:
            logging.debug("Error getting transit route")
            feature.append(sys.maxint, sys.maxint)
        
        logging.debug("Feature set transit: " + str(feature))
        return feature
    
    def build_feature_set(self, start, destination, timestamp):
        res = {}
        feature = []

        feature.append(start)
        feature.extend(self.get_route_car(start, destination, timestamp))
        feature.extend(self.get_route_bike(start, destination, timestamp))
        feature.extend(self.get_route_transit(start, destination, timestamp))

        logging.debug("Featureset: " + str(feature))
        return feature

class Reasoning: 

    def __init__(self):
        pass 

    def train_model(self, feature_list, type):
        logging.debug("Train ML model")
        
        return True

    def recommendation(self, feature_list):
        val = {}
        recommendation = {}

        val['car'] = randint(0, 9)
        val['bike'] = randint(0,9)
        val['transit'] = randint(0,9)

        recommendation['recommendation'] = max(val, key=val.get)

        # Call ML backend

        return recommendation








