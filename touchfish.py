import requests
from app import tfdataservice

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
    ):
        url = self.url_prefix + '/fish/search'
        return requests.get(url=url, params={
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
    
    def add_fish (
        self,
        value: bytes,
        type: str,
        description: str = None,
        tags: str = None,
        extra_info: str = None,
    ):
        url = self.url_prefix + '/fish/add'
        return requests.post(url=url, data={
            'type': type,
            'description': description,
            'tags': tags,
            'extra_info': extra_info,
        }, files={
            'value': value,
        })
    
    def fetch_resource (
        self,
        identity: str
    ):
        url = self.url_prefix + '/resource/fetch'
        return requests.get(url=url, params={
            'identity': identity,
        })

        