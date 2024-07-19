from .definition import FishResp, FishType, tags_parse_str, RespStatus
from yfunc import *
from enum import Enum
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
        import requests
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
        is_marked: bool = False,
        is_locked: bool = False,
        extra_info: str = None,
    ) -> TFResp:
        url = self.url_prefix + '/fish/add'
        tags = tags_parse_str(tags)
        import requests
        res = requests.post(url=url, data={
            'type': type,
            'description': description,
            'tags': tags,
            'is_marked': '1' if is_marked else '0',
            'is_locked': '1' if is_locked else '0',
            'extra_info': extra_info,
        }, files={
            'value': value,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def modify_fish (
        self,
        identity: str, 
        description: str = None,
        tags: list[list[str]] = None,
        extra_info: str = None,
    ) -> TFResp:
        url = self.url_prefix + '/fish/modify'
        tags = tags_parse_str(tags)
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
            'description': description,
            'tags': tags,
            'extra_info': extra_info,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def mark_fish(self, identity: str) -> TFResp:
        url = self.url_prefix + '/fish/mark'
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def unmark_fish(self, identity: str) -> TFResp:
        url = self.url_prefix + '/fish/unmark'
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def lock_fish(self, identity: str) -> TFResp:
        url = self.url_prefix + '/fish/lock'
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def unlock_fish(self, identity: str) -> TFResp:
        url = self.url_prefix + '/fish/unlock'
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)
    
    def remove_fish(self, identity: str) -> TFResp:
        url = self.url_prefix + '/fish/remove'
        import requests
        res = requests.post(url=url, data={
            'identity': identity,
        })
        res_dict = ystr(res.text).json().to_dic()
        return TFResp(res_dict)

    def fetch_resource(self, identity: str) -> bytes:
        url = self.url_prefix + '/resource/fetch'
        import requests
        res = requests.get(url=url, params={
            'identity': identity,
        })
        return res.content
    
    def fetch_preview(self, identity: str) -> bytes:
        url = self.url_prefix + '/resource/preview'
        import requests
        res = requests.get(url=url, params={
            'identity': identity,
        })
        return res.content

class RecipeViewType(Enum):
    empty = 1
    error = 2
    text = 3
    list1 = 4
    list2 = 5

class RecipeActionType(Enum):
    back = 1
    hide = 2
    copy = 3
    open = 4
    shell = 5

class RecipeActionArgType(Enum):
    plain = 1
    para = 2
    commandBarText = 3
    file = 4
    context = 5

class RecipeActionArg:
    type: RecipeActionArgType
    value: str

    def __init__(self, type: RecipeActionArgType, value: str=None) -> None:
        self.type = type
        self.value = value

class RecipeAction:
    type: RecipeActionType
    arguments: list[RecipeActionArg]

    def __init__(self, type: RecipeActionType, arguments: list[RecipeActionArg]=[]) -> None:
        self.type = type
        self.arguments = arguments

class RecipeViewItem:
    title: str
    description: str
    icon: str
    tags: list[str]
    actions: list[RecipeAction]

    def __init__(self,
        title: str,
        description: str,
        icon: str = None,
        tags: list[str] = [],
        actions: list[RecipeAction] = [],
    ) -> None:
        self.title = title
        self.description = description
        self.icon = icon
        self.tags = tags
        self.actions = actions

class RecipeView:

    default_item_icon: str
    error_message: str
    type: RecipeViewType
    items: list[RecipeViewItem]

    def __init__(self,
            type: RecipeViewType,
            items: list[RecipeViewItem],
            default_item_icon: str = None,
            error_message: str = None,
    ) -> None:
        self.type = type
        self.default_item_icon = default_item_icon
        self.items = items
        self.error_message = error_message

    def show(self):
        import sys
        sys.stdout.write(ystr().json().from_object(self))

class MessageCenter:

    @staticmethod
    def send(level: str, content: str, title: str=None, source: str=None):
        message_dic = {
            'level': level,
            'title': title,
            'content': content,
            'source': source,
        }
        import sys
        sys.stdout.write(ystr().json().from_object(message_dic))
