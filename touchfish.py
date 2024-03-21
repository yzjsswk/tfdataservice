import requests

class touchfish:

    url_prefix = 'http://127.0.0.1:5000'

    def search_fish(
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
        url = touchfish.url_prefix + '/fish/search'
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
        value: bytes,
        type: str,
        description: str = None,
        tags: str = None,
        extra_info: str = None,
    ):
        url = touchfish.url_prefix + '/fish/add'
        return requests.post(url=url, data={
            'type': type,
            'description': description,
            'tags': tags,
            'extra_info': extra_info,
        }, files={
            'value': value,
        })

        