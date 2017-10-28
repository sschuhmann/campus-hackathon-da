from sklearn.neural_network import MLPClassifier
from twython import Twython
import pickle
import os.path
import numpy as np

def feedback(requestframe, vehicle):
    # receive the actual transport vehicle that was taken

    location = requestframe[0]
    # dataframe creation
    dataframe = create_dataframe(requestframe, vehicle)
    #add dataframe to the data table
    writeFrame(dataframe)

    # load ml classifier
    if not os.path.isfile('model/classifier.pickle'):
        #create classifier
        classifier = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(20,20), random_state=1)
    else:
        #load classifier
        f = open('model/classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()

    # update the ml-classifier
    print(dataframe)
    X = [dataframe[key] for key in removekey(dataframe, 'vehicle').keys()]
    X = [[x] for x in X]
    X = np.array(X)
    print(X)

    y = [dataframe['vehicle']]
    classifier.partial_fit(X,y, [1,2,3])

    #store the classifier in /model
    f = open('model/classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    return ''

def models_opinion(requestframe):

    #create dataframe
    dataframe = create_dataframe(requestframe, '')
    X = removekey(dataframe, 'vehicle')

    #load classifier
    f = open('model/classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    return classifier.predict(X) #TODO Formulate Prediction for Backend


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
    dataframe['StauScore'] = recent_schlagwort_score('stau', location)
    dataframe['DBVerspätungsScore'] = recent_schlagwort_score('Bahn Verspätung', location)
    dataframe['FerienScore'] = recent_schlagwort_score('Ferien', location)
    dataframe['Feiertag'] = recent_schlagwort_score('Feiertag', location)
    dataframe['Sonnig'] = recent_schlagwort_score('Sonnig', location)
    dataframe['Regen'] = recent_schlagwort_score('Regen', location)
    dataframe['Schnee'] = recent_schlagwort_score('Schnee', location)
    dataframe['Sturm'] = recent_schlagwort_score('Feiertag', location)
    dataframe['Verkehr'] = recent_schlagwort_score('Verkehr', location)
    dataframe['Fahrrad'] = recent_schlagwort_score('Fahrrad', location)
    dataframe['Auto'] = recent_schlagwort_score('Auto', location)
    dataframe['Bahn'] = recent_schlagwort_score('Bahn', location)

    #set vehicle
    if vehicle == 'Car':
        vehicle = 0
    if vehicle == 'Bike':
        vehicle == 1
    if vehicle == 'Train':
        vehicle = 3
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

# for testing: feedback(['Darmstadt', 2334, 35147, 6022, 31518, 1080, 30066], 'Car')
