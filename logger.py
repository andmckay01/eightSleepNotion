import logging

logging.basicConfig(
    filename='api_out.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

log = logging.getLogger(__name__)
