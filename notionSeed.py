# notionSeed isn't a seed in the traditional sense because we do not need notionData.json for things to work
# however, we do need it to make informated decisions about our requests to the notion api
# this is included in case we need it in the future

import requests as req
import json
import env

token = env.notionToken
database_id = env.notionDatabaseId

url = f"https://api.notion.com/v1/databases/{database_id}/query"

payload = {
    "page_size": 10
}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {token}"
}

# notion api request
response = req.post(url, json=payload, headers=headers)
data = json.loads(response.text)

with open("notionData.json", "w") as f:
    json.dump(data, f, indent=1)
