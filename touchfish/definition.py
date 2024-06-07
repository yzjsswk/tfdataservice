from enum import Enum

class FishType(Enum):
    txt = 1
    tiff = 2
    png = 3
    jpg = 4
    pdf = 5
    other = 99

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

class FishResp:

    def __init__(self, 
            id: str, identity: str, type: str, byte_count: int, preview: bytes,
            description: str, tags: list[list[str]], is_marked: bool, is_locked: bool,
            extra_info: str, create_time: str, update_time: str
        ) -> None:
        self.id = id
        self.identity = identity
        self.type = type
        self.byte_count = byte_count
        self.preview = preview
        self.description = description
        self.tags = tags
        self.is_marked = is_marked
        self.is_locked = is_locked
        self.extra_info = extra_info
        self.create_time = create_time
        self.update_time = update_time
        
    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)

    # @staticmethod
    # def from_row(row: tuple) -> 'FishResp':  
    #     return FishResp(
    #         id = row[0],
    #         identity = row[1],
    #         type = row[2],
    #         byte_count=row[3],
    #         preview=None,
    #         description = row[4],
    #         tags = str_parse_tags(row[5]),
    #         is_marked = True if row[6] == 1 else False,
    #         is_locked = True if row[7] == 1 else False,
    #         extra_info = row[8], 
    #         create_time = row[9], 
    #         update_time = row[10],
    #     )
        
    # @staticmethod
    # def from_rows(rows: list[tuple]) -> list['FishResp']:
    #     res = []
    #     for row in rows:
    #         try:
    #             res.append(FishResp.from_row(row))
    #         except Exception as e:
    #             # todo: Note may print long bytes
    #             e.add_note(f"Note: row={row}")
    #             logger.exception(f'error when parse fish from db record, ignore record', e)
    #     return res

def get_dict_resp(status: RespStatus, message: str, extra: str=''):
    from yfunc import ystr
    return {
        'code': status.value + ''.join([s[0] for s in ystr(message).split(remove_null=True)]).upper() + extra,
        'status': status.name,
        'msg': message,
    }

def tags_parse_str(tags: list[list[str]]) -> str:
    from yfunc import ylist
    if tags == None:
        return None
    res = []
    for tag_group in tags:
        tag_group = [t for tag in tag_group if (t:=tag.strip()) != '']
        if len(tag_group) > 0:
            tag_group = ylist(tag_group).unique().sort()
            res.append(','.join(tag_group))
    return '|'.join(res)

def str_parse_tags(tag_str: str) -> list[list[str]]:
    from yfunc import ystr, ylist
    if tag_str == None:
        return None
    res = []
    if tag_str == '':
        return res 
    tag_groups = tag_str.split('|')
    for tag_group in tag_groups:
        cur = ystr(tag_group).split(',', trim_each=True, remove_null=True)
        if len(cur) > 0:
            cur = ylist(cur).unique().sort()
            res.append(cur)
    return res

