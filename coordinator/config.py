import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(100)
logging.getLogger("urllib3.connectionpool").setLevel(100)

port = 6666
host = '0.0.0.0'
