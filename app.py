from yfunc import *
from tfwebserver import tfwebserver
from config import Config
import os

class tfdataservice:
    
    def run(workpath: str, port=5000):
        if not os.path.exists(workpath) or not os.path.isdir(workpath):
            raise Exception('workpath not exists or invalid')
        Config.init_with_workpath(workpath)
        if not os.path.exists(Config.path__log):
            os.makedirs(Config.path__log)
        if not os.path.exists(Config.path__fishdata):
            os.makedirs(Config.path__fishdata)
        if not os.path.exists(Config.path__fishdata__active):
            os.makedirs(Config.path__fishdata__active)
        if not os.path.exists(Config.path__fishdata__expired):
            os.makedirs(Config.path__fishdata__expired)
        if not os.path.exists(Config.path__db):
            # todo: create db and table
            pass
        logger.remove(None)
        logger.add(lambda message: print(message))
        logger.add(Config.path__log + "/{time:YYYY-MM-DD}.log", rotation="00:00")
        # todo: run task
        tfwebserver.run(host='0.0.0.0', port=port)
