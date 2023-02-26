import logger as l
import json
import requests as req
import env
from datetime import datetime as dt
# from pyeight.eight import EightSleep # did things myself instead


# THIS GIVES US THE MOST RECENT CREATED PAGE, MIGHT BE ABLE TO USE IT LATER BUT IT'S PROBABLY A GOOD IDEA TO CHECK THINGS
print('---------THAT NEW NEW---------')

# with open('notionData.json', 'r') as f:
#     data = json.load(f)
#     print(data['results'][0])

token = env.notionToken
database_id = env.notionDatabaseId
url = "https://api.notion.com/v1/pages"

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
    # properties parameer must confrom to the parent database's property schema
    "properties": {
        "Date": {
            "id": "*%24DM",
            "type": "date",
            "date": {
                    "start": "2023-02-26",
                    "end": None,
                    "time_zone": None
            }
        }
    }
}

response = req.post(url, data=json.dumps(body), headers=headers)

print(response.text)
