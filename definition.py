from yfunc import *
from enum import Enum

class FishType(Enum):
    text = 1
    image = 2

    @staticmethod
    def from_name(name: str) -> 'FishType':
        for e in FishType:
            if e.name == name:
                return e
        return None
    
class RespStatus(Enum):
    success = 'S'
    skip = 'P'
    fail = 'F'

class Fish:

    def __init__(self, row: tuple) -> None:  
        self.id = row[0]  
        self.identity = row[1] 
        self.type = row[2]
        if self.type == 'text':
            if isinstance(row[3], str):
                self.value = row[3]
            else:
                try:
                    self.value = ybytes(row[3]).to_str()
                except:
                    self.value = None
        else:
            self.value = None
        self.description = row[4] 
        self.tags = [] if row[5] == '' else row[5].split(',') 
        self.is_marked = True if row[6] == 1 else False
        self.is_locked = True if row[7] == 1 else False
        self.extra_info = row[8] 
        self.create_time = row[9] 
        self.update_time = row[10]
        
    @staticmethod
    def from_rows(rows: list[tuple]) -> list['Fish']:
        res = []
        for row in rows:
            try:
                res.append(Fish(row))
            except Exception as e:
                # todo: Note may print long bytes
                e.add_note(f"Note: row={row}")
                logger.exception(f'error when parse fish from db record, ignore record', e)
        return res
    
def get_dict_resp(status: RespStatus, message: str, extra: str=''):
    return {
        'code': status.value + ''.join([s[0] for s in ystr(message).split(remove_null=True)]).upper() + extra,
        'status': status.name,
        'msg': message,
    }



