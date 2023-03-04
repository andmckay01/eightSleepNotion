FROM python:3.9

ADD eightSleepSession.json env.py functions.py logger.py main.py requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "python", "./main.py" ]