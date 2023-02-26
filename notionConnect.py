import requests as req
import json
import env

token = env.notionToken
database_id = '23b87a29080f4644bf3c0680da72dc01'

url = f"https://api.notion.com/v1/databases/{database_id}/query"

payload = {
    "page_size": 100
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
