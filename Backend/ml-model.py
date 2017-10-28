import time
import json
import datetime
from twython import Twython

def feedback(vehicle, location):
    # receive the actual transport vehicle that was taken

    # dataframe creation
    create_dataframe(location, vehicle)
    # create a date entry and add it to the data table


    # update the ml-model
    return ''

def models_opinion(location):
    return ''#


def create_dataframe(location, vehicle):
    dataframe = {}

    #get Weekday
    datetime_object = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
    weekday = datetime_object.tm_wday
    dataframe['Weekday'] = weekday

    #get Daytime
    minutes_since_midnight = datetime_object.tm_hour*60 + datetime_object.tm_min
    dataframe['Daytime'] = minutes_since_midnight

    #get twitter data
    dataframe['StauScore'] = recent_schlagwort_score('stau', location)
    dataframe['DBVerspätungsScore'] = recent_schlagwort_score('Bahn Verspätung', location)
    dataframe['FerienScore']recent_schlagwort_score('Ferien', location)
    dataframe['Feiertag'] recent_schlagwort_score('Feiertag', location)

    #set vehicle
    dataframe['vehicle'] = vehicle

    return dataframe

def twitter_request(term):
    APP_KEY = 'fVBd5lXoImbrNZcGnKUnAlKeX'
    APP_SECRET = '6wyNQs38QTE0np14pux4UnFADOxYMXCOIKircZOapGmbonjnmB'
    OAUTH_TOKEN = '826760068427292673-jSmNOUwldwlPJyDaisH8Gh834dJZsZP'
    OAUTH_TOKEN_SECRET = 'xoXwefgXOOhasrjUHaNgxZppBbgWBQtOFRLYNNoXw44iJ'
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return twitter.search(q=term, result_type='new', lang='de', count=100)

def recent_schlagwort_score(schlagwort, location):
    search_result = twitter_request(schlagwort)

    count = 0
    for status in search_result['statuses']:
        latest = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
        current = time.strptime(status['created_at'][:19], '%a %b %d %H:%M:%S')
        if current.tm_mon==latest.tm_mon and latest.tm_mday==current.tm_mday and (latest.tm_hour*60+latest.tm_min - current.tm_hour*60+current.tm_min) < 240:
            count += 1
            if location in status['text']:
                count += 2

    return count/100
