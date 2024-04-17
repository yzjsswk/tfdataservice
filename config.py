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

    max_size__fish_save_to_db = 10 * 1024 * 1024 # 10MB

    def init_with_workpath(workpath: str):
        Config.work_path = workpath
        Config.path__db = os.path.join(workpath, 'tf.db')
        Config.path__config = os.path.join(workpath, 'config.yaml')
        Config.path__log = os.path.join(workpath, 'log')
        Config.path__fishdata = os.path.join(workpath, 'fishdata')
        Config.path__fishdata__active = os.path.join(Config.path__fishdata, 'active')
        Config.path__fishdata__expired = os.path.join(Config.path__fishdata, 'expired')
        Config.load_from_file()
    
    def load_from_file():
        if not os.path.exists(Config.path__config):
            return
        with open(Config.path__config, 'r') as config_file:
            config: dict = yaml.safe_load(config_file)
        if 'max_size__fish_save_to_db' in config:
            Config.max_size__fish_save_to_db = config['max_size__fish_save_to_db']
    