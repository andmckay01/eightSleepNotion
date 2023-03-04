from functions import *
import logger as l


# this is the only function we will set a daily trigger for in our cloud environment
def main():
    l.log.debug('Function: main - invoked')
    session8SlpStart()  # loads our current session or starts a new one

    data = pull8SlpData()  # pulls our 8 sleep data
    timestamp = data["timestamp"]
    score = data["score"]
    respRate = data["respRate"]
    heartRate = data["heartRate"]

    postNotion(score, respRate, heartRate)


main()
