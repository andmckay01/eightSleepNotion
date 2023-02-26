import requests as req
import os
import json
from datetime import datetime as dt
from dotenv import load_dotenv

# get from .env file
load_dotenv()
email = os.getenv('eightSleepEmail')
password = os.getenv('eightSleepPassword')
userId = os.getenv('eightSleepUserId')
bedId = os.getenv('eightSleepBedId')

# sends post request, parses data, then writes to session.json


def sessionStart():
    print('invoked sessionStart function')
    response = req.post(
        'https://client-api.8slp.net/v1/login',
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": "okhttp/3.6.0",
            "authority": "app-api.8slp.net"
        },
        data={
            "email": email,
            "password": password
        }
    )
    sessionDict = json.loads(response.text)['session']
    with open("session.json", "w") as file:
        json.dump(sessionDict, file)
    return sessionDict
