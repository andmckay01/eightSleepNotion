import json
import os
import requests as req
from dotenv import load_dotenv

path = "/Users/mckayanderson/Documents/catacombs/devInTraining/eighSleepNotion"

load_dotenv()
notionToken = os.getenv('notionToken')
token = notionToken
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
# response = req.post(url, json=payload, headers=headers)

# don't need to write the file again for tesing purposes
# data = json.loads(response.text)
# file = open("notionData.json", "w")

# with open("notionData.json", "w", encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=1)
