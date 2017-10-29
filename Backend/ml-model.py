import time
import json
import datetime
from sklearn.neural_network import MLPClassifier
from twython import Twython
import pickle
import os.path
import numpy as np
import random
import keras
from keras.models import Sequential
from keras.layers import Dense


def feedback(requestframe, vehicle):
    # receive the actual transport vehicle that was taken

    location = requestframe[0]
    # dataframe creation
    dataframe = create_dataframe(requestframe, vehicle)
    #add dataframe to the data table
    writeFrame(dataframe)
    set = True
    # load ml classifier
    if not os.path.isfile('model/classifier'):
        #create classifier
        classifier = Sequential()
        classifier.add(Dense(1, input_dim=20, activation='relu'))
        classifier.add(Dense(8, activation='relu'))
        classifier.add(Dense(3, activation='softmax'))
        classifier.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    else:
        #load classifier
        classifier = keras.models.load_model('model/classifier')

    # update the ml-classifier
    X = [[dataframe[key] for key in removekey(dataframe, 'vehicle').keys()]]

    y = [dataframe['vehicle']]

    classifier.fit(np.array(X),np.array(y),epochs=1, batch_size=1)

    #store the classifier in /model

    classifier.save('model/classifier')
    return ''

def models_opinion(requestframe):

    #create dataframe
    dataframe = create_dataframe(requestframe, '')
    X = [[dataframe[key] for key in removekey(dataframe, 'vehicle').keys()]]

    #load classifier
    classifier = keras.models.load_model('model/classifier')

    decision = classifier.predict(np.array(X)).tolist() #TODO Formulate Prediction for Backend
    decision_dict = {}
    decision_dict['car'] = decision[0]
    decision_dict['bike'] = decision[1]
    decision_dict['transit'] = decision[2]
    return decision


def create_dataframe(requestframe, vehicle):
    dataframe = {}
    location = requestframe[0]
    dataframe['rq1'] = requestframe[1]
    dataframe['rq2'] = requestframe[2]
    dataframe['rq3'] = requestframe[3]
    dataframe['rq4'] = requestframe[4]
    dataframe['rq5'] = requestframe[5]
    dataframe['rq6'] = requestframe[6]

    #get Weekday
    datetime_object = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
    weekday = datetime_object.tm_wday
    dataframe['Weekday'] = weekday

    #get Daytime
    minutes_since_midnight = datetime_object.tm_hour*60 + datetime_object.tm_min
    dataframe['Daytime'] = minutes_since_midnight

    #get twitter data
    #dataframe['StauScore'] = recent_schlagwort_score('stau', location)
    #dataframe['DBVerspaetungsScore'] = recent_schlagwort_score('Bahn Verspaetung', location)
    #dataframe['FerienScore'] = recent_schlagwort_score('Ferien', location)
    #dataframe['Feiertag'] = recent_schlagwort_score('Feiertag', location)
    #dataframe['Sonnig'] = recent_schlagwort_score('Sonnig', location)
    #dataframe['Regen'] = recent_schlagwort_score('Regen', location)
    #dataframe['Schnee'] = recent_schlagwort_score('Schnee', location)
    #dataframe['Sturm'] = recent_schlagwort_score('Feiertag', location)
    #dataframe['Verkehr'] = recent_schlagwort_score('Verkehr', location)
    #dataframe['Fahrrad'] = recent_schlagwort_score('Fahrrad', location)
    #dataframe['Auto'] = recent_schlagwort_score('Auto', location)
    #dataframe['Bahn'] = recent_schlagwort_score('Bahn', location)
    dataframe['StauScore'] = random.randrange(0, 1)
    dataframe['DBVerspaetungsScore'] = random.randrange(0, 1)
    dataframe['FerienScore'] = random.randrange(0, 1)
    dataframe['Feiertag'] = random.randrange(0, 1)
    dataframe['Sonnig'] = random.randrange(0, 1)
    dataframe['Regen'] = random.randrange(0, 1)
    dataframe['Schnee'] = random.randrange(0, 1)
    dataframe['Sturm'] = random.randrange(0, 1)
    dataframe['Verkehr'] = random.randrange(0, 1)
    dataframe['Fahrrad'] = random.randrange(0, 1)
    dataframe['Auto'] = random.randrange(0, 1)
    dataframe['Bahn'] = random.randrange(0, 1)

    #set vehicle
    if vehicle == 'car':
        vehicle = [1,0,0]
    if vehicle == 'bike':
        vehicle = [0,1,0]
    if vehicle == 'transit':
        vehicle = [0,0,1]
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

    return count/300

def writeFrame(dataframe):
    string_dataframe = ''
    for key in dataframe.keys():
        string_dataframe += key + ':' + str(dataframe[key]) + ','

    f = open('datatable', 'a')
    f.write(string_dataframe + '\n')  # python will convert \n to os.linesep
    f.close()

def read_dataset():
    return ''

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r
