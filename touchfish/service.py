from .storage import DataBase, FileSystem, FishIndex, logger
from .definition import *
from .config import Config
from yfunc import *

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
        DataBase.request__insert(request_id, url, time_cost, origin_input, real_input, response, extra_info)

    @staticmethod
    def update_request_time (
        request_id: str,
        time_cost_info: dict,
    ) -> None:
        DataBase.request__update_time(request_id, ystr().json().from_object(time_cost_info))
        
    @staticmethod
    def statistic() -> dict:
        _, res = DataBase.fish__search()
        type_stats = {}
        tag_stats = {}
        mark_stats = {'marked':0, 'unmarked':0}
        lock_stats = {'locked':0, 'unlocked':0}
        for r in res:
            if r.type in type_stats:
                type_stats[r.type] += 1
            else:
                type_stats[r.type] = 1
            for t in ylist(r.tags).flatten():
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
            identity: list[str] = None, # match any
            type: list[FishType] = None, # match any
            tags: list[list[str]] = None, # match each
            is_marked: bool = None,
            is_locked: bool = None,
            page_num: int = None,
            page_size: int = None,
            with_preview: bool = None,
        ) -> tuple[int, list[FishResp]]:
        if type != None:
            type = [e.name for e in type]
        if tags != None:
            tags = ylist(tags).flatten()
        if is_marked != None:
            is_marked = 1 if is_marked else 0
        if is_locked != None:
            is_locked = 1 if is_locked else 0
        if fuzzys != None:
            # use fuzzy(ignore value and description), match value or descrption
            identity__value_hits = FishIndex.search_document(fuzzys)
            total_count, fish = DataBase.fish__search(
                value_identity=identity__value_hits, identity=identity, description=fuzzys,
                type=type, tags=tags, is_marked=is_marked, is_locked=is_locked,
                page_num=page_num, page_size=page_size, 
            )
        else:
            # use value and description(ignore fuzzy), match value and description
            if value != None:
                identity__value_hits = FishIndex.search_document(value)
                if identity != None:
                    identity = ylist(identity).inter(identity__value_hits)
                else:
                    identity = identity__value_hits
            total_count, fish = DataBase.fish__search(
                identity=identity, description=description,
                type=type, tags=tags, is_marked=is_marked, is_locked=is_locked,
                page_num=page_num, page_size=page_size, 
            )
        # todo: change preview to preview in db
        if with_preview:
            for f in fish:
                if f.type != 'txt':
                    continue
                try:
                    fishdata = FileSystem.fishdata__read(f.identity)
                    if fishdata == None:
                        logger.warning(f'fish exists in db but fishdata not found, ignore preview, identity = {f.identity}')
                    else:    
                        f.preview = ybytes(fishdata).to_str()
                except:
                    logger.warning(f'parse text fish data to str fail, ignore preview, identity = {f.identity}')
        return total_count, fish
    
    @staticmethod
    def add_fish (
            value: bytes,
            description: str,
            type: FishType,
            tags: list[list[str]],
            is_marked: bool,
            is_locked: bool,
            extra_info: str,
        ) -> dict:
        if value == None:
            return get_dict_resp(RespStatus.fail, 'value can not be null', 'SVAF')
        if type == None:
            return get_dict_resp(RespStatus.fail, 'type can not be null or invalid', 'SVAF')
        identity = ybytes(value).md5()
        if DataBase.fish__exist(identity):
            return get_dict_resp(RespStatus.fail, 'fish data exists', 'SVAF')
        tags = tags_parse_str(tags)
        if extra_info == None:
            extra_info_dic = {}
        else:
            extra_info_dic = ystr(extra_info).json().to_dic()
        match type:
            case FishType.txt:
                text_value = ybytes(value).to_str()
                extra_info_dic['char_count'] = len(text_value)
                extra_info_dic['word_count'] = len(text_value.to_words())
                extra_info_dic['row_count'] = len(text_value.to_rows())
                preview = text_value[:2000]
            case FishType.tiff | FishType.png | FishType.jpg:
                image_value = ypic().from_bytes(value)
                extra_info_dic['width'] = image_value.p.width
                extra_info_dic['height'] = image_value.p.height
                preview = image_value.resize(width=512, height=None).to_bytes()
            case FishType.pdf:
                import fitz
                pdf = fitz.open(stream=bytes(value))
                extra_info_dic['page_count'] = pdf.page_count
                if pdf.page_count > 0:
                    first_page = pdf.load_page(0)
                    image__first_page = first_page.get_pixmap()
                    pic = ypic().from_bytes(image__first_page.tobytes())
                    preview = pic.resize(width=512, height=None).to_bytes()
                else:
                    logger.warning('save pdf fish - preview=None: page_count <= 0')
                    preview = None
            case _:
                logger.warning(f'add fish - preview=None: type not support preview, type={type}')
                preview = None
        extra_info = ystr().json().from_object(extra_info_dic)
        if preview != None and len(preview) > Config.preview_size_limit:
            logger.warning(f'add fish - ignore preview: preview size too large, len(preview)={len(preview)}, limit={Config.preview_size_limit}')
            preview = None
        FileSystem.fishdata__save(value, type)
        if type == FishType.txt:
            FishIndex.add_document(identity, ybytes(value).to_str())
        DataBase.fish__insert(
            identity=identity, type=type.name, byte_count=len(value), preview=preview,
            description=description, tags=tags, is_marked=is_marked, is_locked=is_locked, extra_info=extra_info,
        )
        return get_dict_resp(RespStatus.success, identity, 'SVAF')
    
    @staticmethod
    def remove_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.skip, 'fish not exists', 'SVRF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVRF')
        FileSystem.fishdata__expire(identity)
        FishIndex.remove_document(identity)
        DataBase.fish__delete(id=res[0].id)
        return get_dict_resp(RespStatus.success, identity, 'SVRF')
    
    @staticmethod
    def mark_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVMF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVMF')
        if res[0].is_marked:
            return get_dict_resp(RespStatus.skip, 'fish has been marked', 'SVMF')
        DataBase.fish__update(id=res[0].id, is_marked=1)
        return get_dict_resp(RespStatus.success, identity, 'SVMF')
    
    @staticmethod
    def unmark_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVUMF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVUMF')
        if not res[0].is_marked:
            return get_dict_resp(RespStatus.skip, 'fish is not marked', 'SVUMF')
        DataBase.fish__update(id=res[0].id, is_marked=0)
        return get_dict_resp(RespStatus.success, identity, 'SVUMF')
    
    @staticmethod
    def lock_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVLF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.skip, 'fish has been locked', 'SVLF')
        DataBase.fish__update(id=res[0].id, is_locked=1)
        return get_dict_resp(RespStatus.success, identity, 'SVLF')
    
    @staticmethod
    def unlock_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVULF')
        if not res[0].is_locked:
            return get_dict_resp(RespStatus.skip, 'fish is not locked', 'SVULF')
        DataBase.fish__update(id=res[0].id, is_locked=0)
        return get_dict_resp(RespStatus.success, identity, 'SVULF')
    
    @staticmethod
    def pin_fish(identity: str) -> dict:
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVPF')
        DataBase.fish__update(id=res[0].id, type=res[0].type)
        return get_dict_resp(RespStatus.success, identity, 'SVPF')
    
    @staticmethod
    def modify_fish (
            identity: str, 
            description: str = None,
            tags: list[str] = None,
            extra_info: str = None,
    ) -> dict:
        if description == None and tags == None and extra_info == None:
            return get_dict_resp(RespStatus.skip, 'nothing to update', 'SVMDF')
        _, res = DataBase.fish__search(identity=[identity])
        if len(res) == 0:
            return get_dict_resp(RespStatus.fail, 'fish not exists', 'SVMDF')
        if res[0].is_locked:
            return get_dict_resp(RespStatus.fail, 'fish is locked', 'SVMDF')
        tags = tags_parse_str(tags)
        DataBase.fish__update(id=res[0].id, description=description, tags=tags, extra_info=extra_info)
        return get_dict_resp(RespStatus.success, identity, 'SVMDF')    
    
    @staticmethod
    def clear_fish(second_delta: int) -> list[str]:
        target_ts = int(ystr().timestamp().now()) - second_delta
        ret = []
        to_delete_id = []
        _, fish_list = DataBase.fish__search(is_marked=False, is_locked=False)
        for fish in fish_list:
            if int(ystr(fish.update_time).datetime().to_timestamp()) < target_ts:
                ret.append(fish.identity)
                to_delete_id.append(fish.id)
        DataBase.fish__delete_list(to_delete_id)
        return ret
            
    @staticmethod
    def fetch_resource(identity: str) -> bytes | None:
        return FileSystem.fishdata__read(identity)
    
    @staticmethod
    def fetch_preview(identity: str) -> bytes | None:
        return DataBase.fish__select_preview(identity)
