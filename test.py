import requests as req
import json
import logger as l
import env
import datetime as dt

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

response = req.post(
    'https://client-api.8slp.net/v1/login',
    headers=headersPost8Slp,
    data=data8Slp
)
print(response)

# sessionDict = json.loads(response.text)['session']
# print(sessionDict)
