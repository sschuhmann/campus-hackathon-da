import time
import datetime
from twython import Twython

def feedback(vehicle, location):
    # receive the actual transport vehicle that was taken

    # dataframe creation
    # create a date entry and add it to the data table


    # update the ml-model
    return ''

def models_opinion(location):
    return ''#


def create_dataframe(location):
    dataframe = {}

    #get Weekday
    datetime_object = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
    weekday = datetime_object.tm_wday
    dataframe['Weekday'] = weekday

    #get Daytime
    minutes_since_midnight = datetime_object.tm_hour*60 + datetime_object.tm_min
    dataframe['Daytime'] = minutes_since_midnight

    #get twitter data
    dataframe[''] = twitter_request(location)


    return data

def twitter_request():
    APP_KEY = 'fVBd5lXoImbrNZcGnKUnAlKeX'
    APP_SECRET = '6wyNQs38QTE0np14pux4UnFADOxYMXCOIKircZOapGmbonjnmB'
    OAUTH_TOKEN = '826760068427292673-jSmNOUwldwlPJyDaisH8Gh834dJZsZP'
    OAUTH_TOKEN_SECRET = 'xoXwefgXOOhasrjUHaNgxZppBbgWBQtOFRLYNNoXw44iJ'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter.search(q='python')
