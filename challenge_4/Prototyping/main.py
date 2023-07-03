import logging
import psycopg2
import time

logging.basicConfig(
    format = '______________________\n%(levelname)-2s %(asctime)s \n%(message)s',
    filename = F'.\challenge_4\Prototyping\logs\{datetime.today().strftime("%y.%m.%d")}_py.log', 
    encoding = 'utf-8', 
    level = logging.DEBUG,
    datefmt='%y.%m.%d %H:%M:%S'
    )