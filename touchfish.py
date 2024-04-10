import requests
from app import tfdataservice
from yfunc import *

class tfoperator:

    def __init__(self, host='127.0.0.1', port=5000) -> None:
        self.url_prefix = f'http://{host}:{port}'

    def search_fish (
        self,
        fuzzys: str = None, 
        value: str = None, 
        description: str = None, 
        identity: str = None,
        type: str = None, 
        tags: str = None, 
        is_marked: str = None,
        is_locked: str = None,
        page: str = None,
    ) -> str:
        url = self.url_prefix + '/fish/search'
        res = requests.get(url=url, params={
            'fuzzys': fuzzys,
            'value': value,
            'description': description, 
            'identity': identity,
            'type': type, 
            'tags': tags, 
            'is_marked': is_marked,
            'is_locked': is_locked,
            'page': page,
        })
        return res.text
    
    def add_fish (
        self,
        value: bytes,
        type: str,
        description: str = None,
        tags: str = None,
        extra_info: str = None,
    ) -> str:
        url = self.url_prefix + '/fish/add'
        res = requests.post(url=url, data={
            'type': type,
            'description': description,
            'tags': tags,
            'extra_info': extra_info,
        }, files={
            'value': value,
        })
        return res.text
    
    def fetch_resource (
        self,
        identity: str
    ) -> bytes:
        url = self.url_prefix + '/resource/fetch'
        res = requests.get(url=url, params={
            'identity': identity,
        })
        return res.content

        