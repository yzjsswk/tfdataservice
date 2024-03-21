from yfunc import *
from tfwebserver import tfwebserver
from config import Config

class tfdataservice:

    def __init_logger__():
        logger.remove(None)
        logger.add(lambda message: print(message))
        logger.add(Config.path__log + "/{time:YYYY-MM-DD}.log", rotation="00:00")
    
    def start():
        tfdataservice.__init_logger__()
        tfwebserver.run()
