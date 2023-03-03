import logging

# configure the logging module
logging.basicConfig(filename='example.log', level=logging.DEBUG,
                    format='%(asctime)s:%(message)s')

# log some data
logging.debug('This is a debug message.')
logging.info('This is an info message.')
logging.warning('This is a warning message.')
logging.error('This is an error message.')
logging.critical('This is a critical message.')
