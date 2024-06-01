from .app import tfdataservice
from .definition import *
import requests
from yfunc import *
from typing import Any

class PageInfo:

    page_num: int
    page_size: int
    total_page: int
    total_count: int

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class TFResp:

    time_cost: int
    code: str
    status: str
    msg: str
    data: Any | None

    def __init__(self, res_dict: dict) -> None:
        self.time_cost = res_dict.get('time_cost', None)
        self.code = res_dict.get('code', None)
        self.status = res_dict.get('status', None)
        self.msg = res_dict.get('msg', None)
        self.data = res_dict.get('data', None)
        if self.data != None:
            page = PageInfo()
            page.page_num = self.data.get('page_num', None)
            page.page_size = self.data.get('page_size', None)
            page.total_page = self.data.get('total_page', None)
            page.total_count = self.data.get('total_count', None)
            fish = self.data.get('fish', None)
            fish_resp = [
                FishResp(
                    id = f.get('id', None),
                    identity = f.get('identity', None),
                    type = f.get('type', None),
                    byte_count = f.get('byte_count', None),
                    preview = f.get('preview', None),
                    description = f.get('description', None),
                    tags = f.get('tags', None),
                    is_marked = f.get('is_marked', None),
                    is_locked = f.get('is_locked', None),
                    extra_info = f.get('extra_info', None),
                    create_time = f.get('create_time', None),
                    update_time = f.get('update_time', None),
                ) for f in fish
            ] if fish != None else None
                
            self.data = (page, fish_resp)

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class tfoperator:

    # todo: para should not be str

    def __init__(self, host='127.0.0.1', port=5000) -> None:
        self.url_prefix = f'http://{host}:{port}'

    def search_fish (
        self,
        fuzzys: str = None, 
        value: str = None, 
        description: str = None, 
        identity: str = None,
        type: list[FishType] = None, 
        tags: list[list[str]] = None, 
        is_marked: bool = None,
        is_locked: bool = None,
        page_num: int = 1,
        page_size: int = 10,
        with_preview: bool = True,
    ) -> TFResp:
        url = self.url_prefix + '/fish/search'
        if type != None:
            type = ','.join(t.name for t in type)
        tags = tags_parse_str(tags)
        if is_marked != None:
            is_marked = 'true' if is_marked else 'false'
        if is_locked != None:
            is_locked = 'true' if is_locked else 'false'
        page_num = str(page_num)
        page_size = str(page_size)
        if with_preview != None:
            with_preview = 'true' if with_preview else 'false'
        res = requests.get(url=url, params={
            'fuzzys': fuzzys,
            'value': value,
            'description': description, 
            'identity': identity,
            'type': type, 
            'tags': tags, 
            'is_marked': is_marked,
            'is_locked': is_locked,
            'page_num': page_num,
            'page_size': page_size,
            'with_preview': with_preview,
        })
        if res.status_code != 200:
            raise Exception(f'request error: {res.text}')
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def add_fish (
        self,
        value: bytes,
        type: str,
        description: str = None,
        tags: list[list[str]] = None,
        extra_info: str = None,
    ) -> str:
        url = self.url_prefix + '/fish/add'
        tags = tags_parse_str(tags)
        res = requests.post(url=url, data={
            'type': type,
            'description': description,
            'tags': tags,
            'extra_info': extra_info,
        }, files={
            'value': value,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def fetch_resource (
        self,
        identity: str
    ) -> bytes:
        url = self.url_prefix + '/resource/fetch'
        res = requests.get(url=url, params={
            'identity': identity,
        })
        return res.content

        