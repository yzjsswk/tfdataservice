class Config:
    work_path = '/Users/yzjsswk/WorkSpace/tfdataservice'
    db_name = 'tf.db'
    path__db = work_path + '/' + db_name
    path__resource = work_path + '/resource'
    path__log = work_path + '/log'
    max_size__fish_save_to_db = 10 * 1024 * 1024 # 10MB
    