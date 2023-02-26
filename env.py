import os
from dotenv import load_dotenv

# get from .env file
load_dotenv()
email = os.getenv('eightSleepEmail')
password = os.getenv('eightSleepPassword')
userId = os.getenv('eightSleepUserId')
bedId = os.getenv('eightSleepBedId')
