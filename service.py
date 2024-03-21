from yfunc import *
from db import DB
from definition import *


class Service():

    @staticmethod
    def add_request_log (
        request_id: str,
        url: str,
        time_cost: str,
        origin_input: dict,
        real_input: dict,
        response: dict,
        extra_info: str
    ) -> None:
        origin_input = ystr().json().from_object(origin_input)
        if 'value' in real_input:
            real_input['value'] = str(real_input['value'])
        real_input = ystr().json().from_object(real_input)
        response = ystr().json().from_object(response)
        DB.request__insert(request_id, url, time_cost, origin_input, real_input, response, extra_info)

    @staticmethod
    def update_request_time (
        request_id: str,
        time_cost_info: dict,
    ) -> None:
        DB.request__update_time(request_id, ystr().json().from_object(time_cost_info))
        
    @staticmethod
    def statistic() -> dict:
        res = DB.fish__search()
        type_stats = {}
        tag_stats = {}
        mark_stats = {'marked':0, 'unmarked':0}
        lock_stats = {'locked':0, 'unlocked':0}
        for r in res:
            if r.type in type_stats:
                type_stats[r.type] += 1
            else:
                type_stats[r.type] = 1
            for t in r.tags:
                if t in tag_stats:
                    tag_stats[t] += 1
                else:
                    tag_stats[t] = 1
            if r.is_marked:
                mark_stats['marked'] += 1
            else:
                mark_stats['unmarked'] += 1
            if r.is_locked:
                lock_stats['locked'] += 1
            else:
                lock_stats['unlocked'] += 1
        return {
            'total_count': len(res),
            'type': type_stats,
            'tag': tag_stats,
            'mark': mark_stats,
            'lock': lock_stats,
        }
            
    @staticmethod
    def search_fish (
            fuzzys: str = None, # like value or like desc
            value: str = None, # like
            description: str = None, # like
            identity: str = None,
            type: list[FishType] = None, # match any
            tags: list[str] = None, # match each
            is_marked: bool = None,
            is_locked: bool = None,
            page_num: int = None,
            page_size: int = None,
        ) -> tuple[int, list[Fish]]:
        if type != None:
            type = [e.name for e in type]
        if tags != None:
            tags = ylist(tags).unique().sort()
        if is_marked != None:
            is_marked = 1 if is_marked else 0
        if is_locked != None:
            is_locked = 1 if is_locked else 0
        return DB.fish__search(
            fuzzys=fuzzys, value=value, description=description, identity=identity,
            type=type, tags=tags, is_marked=is_marked, is_locked=is_locked,
            page_num=page_num, page_size=page_size, 
        )
    
    @staticmethod
    def pick_fish(id) -> Fish:
        res = DB.fish__pick(id)
        if len(res) == 0:
            return None
        if len(res) > 1:
            logger.warning(f'fish(id={id}) duplicated in database, ignore others')
        return res[0]
    
    @staticmethod
    def add_fish (
            value: bytes,
            description: str,
            type: FishType,
            tags: list[str],
            extra_info: str,
        ) -> dict:
        if value == None:
            return get_dict_resp(RespStatus.fail, 'value can not be null', 'SVAF')
        if type == None:
            return get_dict_resp(RespStatus.fail, 'type can not be null or invalid', 'SVAF')
        if tags != None:
            tags = ylist(tags).unique().sort()
            tags = ','.join(tags)
        identity = ybytes(value).md5()
        if DB.fish__exist(identity):
            return get_dict_resp(RespStatus.fail, 'data duplicated', 'SVAF')
        # todo: check size and save file
        DB.fish__insert(
            value=value, description=description, identity=identity,
            type=type.name, tags=tags, extra_info=extra_info,
        )
        return get_dict_resp(RespStatus.success, 'success', 'SVAF')
    
    @staticmethod
    def remove_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.skip, 'data not exists', 'SVRF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVRF')
        DB.fish__delete(id=res[0].id)
        return get_dict_resp(RespStatus.success, 'success', 'SVRF')
    
    @staticmethod
    def mark_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVMF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVMF')
        if res[0].is_marked:
            return get_dict_resp(RespStatus.skip, 'fish has been marked', 'SVMF')
        DB.fish__update(id=res[0].id, is_marked=1)
        return get_dict_resp(RespStatus.success, 'success', 'SVMF')
    
    @staticmethod
    def unmark_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVUMF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVUMF')
        if not res[0].is_marked:
            return get_dict_resp(RespStatus.skip, 'fish is not marked', 'SVUMF')
        DB.fish__update(id=res[0].id, is_marked=0)
        return get_dict_resp(RespStatus.success, 'success', 'SVUMF')
    
    @staticmethod
    def lock_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVLF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.skip, 'fish has been locked', 'SVLF')
        DB.fish__update(id=res[0].id, is_locked=1)
        return get_dict_resp(RespStatus.success, 'success', 'SVLF')
    
    @staticmethod
    def unlock_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVULF')
        if not res[0].is_locked:
            return get_dict_resp(RespStatus.skip, 'fish is not locked', 'SVULF')
        DB.fish__update(id=res[0].id, is_locked=0)
        return get_dict_resp(RespStatus.success, 'success', 'SVULF')
    
    @staticmethod
    def pin_fish(identity: str) -> dict:
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVPF')
        DB.fish__update(id=res[0].id, type=res[0].type)
        return get_dict_resp(RespStatus.success, 'success', 'SVPF')
    
    @staticmethod
    def modify_fish (
            identity: str, 
            description: str = None,
            tags: list[str] = None,
            extra_info: str = None,
    ) -> dict:
        if description == None and tags == None and extra_info == None:
            return get_dict_resp(RespStatus.skip, 'nothing to update', 'SVMDF')
        res = DB.fish__search(identity=identity)
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'data not exists', 'SVMDF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVMDF')
        if tags != None:
            tags = ylist(tags).unique().sort()
            tags = ','.join(tags)
        DB.fish__update(id=res[0].id, description=description, tags=tags, extra_info=extra_info)
        return get_dict_resp(RespStatus.success, 'success', 'SVMDF')    
    
    