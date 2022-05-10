import logging

logger_main = logging.getLogger('main')
logger_main.setLevel('INFO')

file_handler = logging.FileHandler('log.log', encoding='utf-8')
format = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
file_handler.setFormatter(format)

logger_main.addHandler(file_handler)


