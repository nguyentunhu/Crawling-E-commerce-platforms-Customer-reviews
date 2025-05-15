import logging

logging.basicConfig(
    filename='logs/crawler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

def get_logger():
    return logging.getLogger(__name__)
