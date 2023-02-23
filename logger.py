import logging
from datetime import datetime
import sys

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler(datetime.now().strftime('%d_%m_%Y.log'))
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
# screen_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(screen_handler)
