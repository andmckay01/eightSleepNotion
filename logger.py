import logging

logging.basicConfig(
    filename='history.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

log = logging.getLogger(__name__)
