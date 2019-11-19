import logging

'''
    Creating a logger with its settings and returning it

    :param: (str) name: name of the logger
'''

def setup_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    logging.basicConfig(filename='../logs/myapp.log', level=logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


'''
    Getting the logger with the given name

    :param: (str) name: name of the logger
'''

def get_logger(name):
    return logging.getLogger(name)
