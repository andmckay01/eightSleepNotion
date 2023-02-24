import email
import requests as req
import json
import os
from datetime import datetime as dt
from dotenv import load_dotenv
# import pyEight

load_dotenv()
email = os.getenv('eightSleepEmail')
password = os.getenv('eightSleepPassword')
userId = os.getenv('eightSleepUserId')
bedId = os.getenv('eightSleepBedId')

url = f"https://app-api.8slp.net/v1/users/USER_ID/alarms/ALARM_ID"

# post request
postHeaders = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "User-Agent": "okhttp/3.6.0",
    "authority": "app-api.8slp.net"
}

apiSession = req.post(
    'https://client-api.8slp.net/v1/login',
    headers=postHeaders,
    data={
        "email": email,
        "password": password
    }
)

sessionObject = json.loads(apiSession.text)
sessionToken = sessionObject['session']['token']
sessionExpiration = dt.strptime(
    sessionObject['session']['expirationDate'],
    "yyyy-MM-dd'T'HH:mm:ss:SSS'Z'")

nowUtc = dt.utcnow()

if sessionExpiration >= nowUtc:
    print('ohhhhhh shit')

else:
    ('looking good')


# post request - done
# parse token out of post request - done
# wrapped in if (only pull the post request if the token is no longer valid)
# let's do it based on the expiration date so we don't have to pull
# use the pull request to get the most recent night of data
# take this and put it into notion
