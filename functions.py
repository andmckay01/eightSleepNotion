import requests as req
import json
import logger as l
import env
import datetime as dt


# body for 8sleep requests
headersPost8Slp = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "User-Agent": "okhttp/3.6.0",
    "authority": "app-api.8slp.net"
}
data8Slp = {
    "email": env.email,
    "password": env.password
}


# loads our session json object and raises exception error if not found
def session8SlpLoad():
    l.log.debug('Function: session8SlpLoad - invoked')
    try:  # will fail if this doesn't exist
        with open('eightSleepSession.json', 'r') as f:
            l.log.debug(
                "Function: session8SlpLoad - loading eightSleepSession.json file")
            data = json.load(f)
            l.log.debug(
                f"Function: session8SlpLoad - successfully loaded session: {data}")
        return {
            "sessionUserId": data['userId'],
            "sessionToken": data['token'],
            "sessionExpiration": dt.datetime.strptime(
                data['expirationDate'],
                "%Y-%m-%dT%H:%M:%S.%fZ")
        }
    except FileNotFoundError:
        l.log.debug("Function: session9SlpLoad - file not found error")
        raise Exception("Session data file not found")
    except (json.JSONDecodError, KeyError, ValueError):
        l.log.debug(
            "Function: session9SlpLoad - session data is invalid or incomplete")
        raise Exception(
            "Session data is invalid or incomplete"
        )


# sends post request, parses data, then writes to eightSleepSession.json
def session8SlpStart():
    l.log.debug('Function: session8SlpStart - invoked')
    # if sessionExpiration is on or before today, reload and rewrite the session object
    if session8SlpLoad()['sessionExpiration'].date() <= dt.datetime.utcnow().date():
        l.log.debug(
            'Function: session8SlpStart - current session <= today, recreating 8 sleep session')
        response = req.post(
            'https://client-api.8slp.net/v1/login',
            headers=headersPost8Slp,
            data=data8Slp
        )
        sessionDict = json.loads(response.text)['session']
        l.log.debug(f'Function: session8SlpStart - new session: {sessionDict}')
        with open("eightSleepSession.json", "w") as file:
            json.dump(sessionDict, file)
        return sessionDict
    else:
        l.log.debug(
            'Function: session8SlpStart - current session is still valid')
        with open('eightSleepSession.json', 'r') as f:
            data = json.load(f)
        l.log.debug(
            f'Function: session8SlpStart - current session: {data}')
        return {
            "sessionUserId": data['userId'],
            "sessionToken": data['token'],
            "sessionExpiration": data['expirationDate']
        }


# pulls the data from the eightsleep api, parses it, returns a data object
def pull8SlpData():
    l.log.debug('Function: pull8SlpData - invoked')

    # ensure we have a valid session
    sessionToken = session8SlpStart()['sessionToken']

    # get request
    response = req.get(
        f'https://client-api.8slp.net/v1/users/{env.userId}/intervals',
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "User-Agent": "okhttp/3.6.0",
            "authority": "app-api.8slp.net",
            "session-token": f"{sessionToken}"
        },
        data=data8Slp
    )

    # parsing the data in the get request
    data = json.loads(response.text)
    score = data['intervals'][0]['score']
    respRate = data['intervals'][0]['timeseries']['respiratoryRate'][0][1]
    heartRateArray = data['intervals'][0]['timeseries']['heartRate']
    heartRateSum = 0
    for value in heartRateArray:
        heartRateSum += value[1]
    heartRateArrayLength = len(heartRateArray)
    heartRate = heartRateSum / heartRateArrayLength  # gives us the average
    timestamp = heartRateArray[heartRateArrayLength - 1][0]
    toReturn = {
        "timestamp": timestamp,
        "score": score,
        "respRate": respRate,
        "heartRate": heartRate
    }
    l.log.debug(f'Function: pull8SlpData - dataPulled: {toReturn}')

    # return of the 4 variables we care about
    return toReturn


# notion post request (must pass in variables from pull8SlpData)
def postNotion(score, respRate, heartRate):
    l.log.debug('Function: postNotion - invoked')
    token = env.notionToken
    database_id = env.notionDatabaseId
    url = "https://api.notion.com/v1/pages"
    today = dt.date.today()

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    body = {
        "parent": {
            "database_id": f"{database_id}"
        },
        # properties parameer must conform to the parent database's property schema
        "properties": {
            "Date": {
                "id": "*%24DM",
                "type": "date",
                "date": {
                        "start": f"{today}",
                        "end": None,
                        "time_zone": None
                }
            },
            "Sleep Data (score | respRate | heartRate)": {
                "id": "rj%40V",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"{score} | "
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": f"{round(respRate, 1)} | "
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": f"{round(heartRate, 1)}"
                        }
                    }
                ]
            }
        }
    }
    response = req.post(url, data=json.dumps(body), headers=headers)
    l.log.debug(f'Function: postNotion - response: {response}')
    return response
