import requests as req
import json
from datetime import datetime as dt
from functions import sessionStart, start
import env
import asyncio
from pyeight.eight import EightSleep

# not used right now
# url = f"https://app-api.8slp.net/v1/users/USER_ID/alarms/ALARM_ID"

with open('session.json', 'r') as f:
    data = json.load(f)  # parses json into a dictionary object

# variables
sessionToken = data['token']
sessionExpiration = dt.strptime(
    data['expirationDate'],
    "%Y-%m-%dT%H:%M:%S.%fZ")
nowUtc = dt.utcnow()

if sessionExpiration <= nowUtc:
    apiSession = sessionStart()
    with open('session.json', 'r') as f:
        data = json.load(f)  # parses json into a dictionary object
else:
    start()
    # insert eightsleep pull request here

# notion section
# 1. Create a new day automatically with this script
# 2. Then take the sleep data and put it into the current day in notion
