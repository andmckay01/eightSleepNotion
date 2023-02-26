import requests as req
import json
import logger as l
import env


# not sure how to get this functionality in the functions file without it always running
def sessionLoad():
    with open('eightSleepSession.json', 'r') as f:
        data = json.load(f)  # parses json into a dictionary object
    return data


# session token (if exists)
try:
    sessionToken = sessionLoad()['token']
except:
    print('no current session available')


# body for post and get requests
headersPost = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "User-Agent": "okhttp/3.6.0",
    "authority": "app-api.8slp.net"
},
headersGet = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "User-Agent": "okhttp/3.6.0",
    "authority": "app-api.8slp.net",
    "session-token": f"{sessionToken}"
}
data = {
    "email": env.email,
    "password": env.password
}


# sends post request, parses data, then writes to eightSleepSession.json
def sessionStart():
    l.log.debug('invoked sessionStart function')
    response = req.post(
        'https://client-api.8slp.net/v1/login',
        headers=headersPost,
        data=data
    )
    sessionDict = json.loads(response.text)['session']
    with open("eightSleepSession.json", "w") as file:
        json.dump(sessionDict, file)
    return sessionDict


# pulls the data from the eightsleep api
def pullData():
    l.log.debug('invoked pullData function')
    response = req.get(
        f'https://client-api.8slp.net/v1/users/{env.userId}/intervals',
        headers=headersGet,
        data=data
    )
    dataDict = json.loads(response.text)
    return dataDict
