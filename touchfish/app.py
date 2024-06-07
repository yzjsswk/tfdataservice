from .web import tfwebserver
from .task import tftask
from .config import Config
from .storage import DataBase, FishIndex, FileSystem, logger
from yfunc import *
import os

class tfdataservice:
    
    def run(workpath: str, port=5000):
        if not os.path.exists(workpath) or not os.path.isdir(workpath):
            raise Exception('workpath not exists or invalid')
        Config.init_with_workpath(workpath)
        if not os.path.exists(Config.path__log):
            os.makedirs(Config.path__log)
        logger.remove(None)
        logger.add(lambda message: print(message))
        logger.add(Config.path__log + "/{time:YYYY-MM-DD}.log", rotation="00:00")
        if not os.path.exists(Config.path__fishdata):
            os.makedirs(Config.path__fishdata)
        if not os.path.exists(Config.path__fishdata__active):
            os.makedirs(Config.path__fishdata__active)
        if not os.path.exists(Config.path__fishdata__expired):
            os.makedirs(Config.path__fishdata__expired)
        if not os.path.exists(Config.path__db):
            with open(Config.path__db, 'w') as _:
                pass
            for sql in DataBase.init_sql:
                ystr(Config.path__db).filepath().db().execute(sql)
        if not os.path.exists(Config.path__fishindex):
            os.makedirs(Config.path__fishindex)
            FishIndex.create_index()
        FishIndex.open_index()
        FileSystem.update_cache()
        if Config.build_index:
            logger.info(f'start building index at {Config.path__fishindex} ...')
            FishIndex.build_index()
            logger.info('finish building index')
        tftask.run()
        tfwebserver.run(host='0.0.0.0', port=port)
