import json
import os
import requests as req
from dotenv import load_dotenv

path = "/Users/mckayanderson/Documents/catacombs/devInTraining/eighSleepNotion"

load_dotenv()
notionToken = os.getenv('notionToken')
token = notionToken
database_id = '23b87a29080f4644bf3c0680da72dc01'
