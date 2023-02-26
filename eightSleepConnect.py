import json
from datetime import datetime as dt
from functions import *
# from pyeight.eight import EightSleep # did things myself instead


with open('eightSleepSession.json', 'r') as f:
    data = json.load(f)  # parses json into a dictionary object

# variables
sessionToken = data['token']
sessionExpiration = dt.strptime(
    data['expirationDate'],
    "%Y-%m-%dT%H:%M:%S.%fZ")
nowUtc = dt.utcnow()


# this is the only function we will set a daily trigger for in our cloud environment
def main():
    # check session and start a new one if needed
    if sessionExpiration <= nowUtc:
        apiSession = sessionStart()
        with open('eightSleepSession.json', 'r') as f:
            data = json.load(f)  # parses json into a dictionary object

    # pull most recent day's data and create our 4 variables
    data = pullData()
    score = data['intervals'][0]['score']
    respRate = data['intervals'][0]['timeseries']['respiratoryRate'][0][1]
    heartRateArray = data['intervals'][0]['timeseries']['heartRate']
    heartRateSum = 0
    for value in heartRateArray:
        heartRateSum += value[1]
    heartRateArrayLength = len(heartRateArray)
    heartRate = heartRateSum / heartRateArrayLength  # gives us the average
    timestamp = heartRateArray[heartRateArrayLength - 1][0]

    l.log.debug(f'timestamp: {timestamp}')
    l.log.debug(f'score: {score}')
    l.log.debug(f'respRate: {respRate}')
    l.log.debug(f'heartRate: {heartRate}')

# create a new day in notion

# put data in that new day in notion

# add logger information to everything so I can troubleshoot when things do eventually go wrong
