import os
import yaml

class Config:

    work_path: str
    path__config: str
    path__db: str
    path__log: str
    path__fishdata: str
    path__fishdata__active: str
    path__fishdata__expired: str
    path__fishindex: str

    build_index = False
    fishindex_id = 'A'

    preview_size_limit = 1048576 # 1MB
    
    def init_with_workpath(workpath: str):
        Config.work_path = workpath
        Config.path__config = os.path.join(workpath, 'config.yaml')
        Config.load_from_file()
        Config.path__db = os.path.join(workpath, 'tf.db')
        Config.path__log = os.path.join(workpath, 'log')
        Config.path__fishdata = os.path.join(workpath, 'fishdata')
        Config.path__fishdata__active = os.path.join(Config.path__fishdata, 'active')
        Config.path__fishdata__expired = os.path.join(Config.path__fishdata, 'expired')
        Config.path__fishindex = os.path.join(os.path.join(workpath, 'fishindex'), Config.fishindex_id)
        
    def load_from_file():
        if not os.path.exists(Config.path__config):
            return
        with open(Config.path__config, 'r') as config_file:
            config: dict = yaml.safe_load(config_file)
        if 'build_index' in config:
            Config.build_index = config['build_index']
        if 'fishindex_id' in config:
            Config.fishindex_id = config['fishindex_id']


