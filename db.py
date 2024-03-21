from yfunc import *
from config import Config
from definition import Fish


class DB:

    fp = ystr(Config.path__db).filepath()

    @staticmethod
    def request__insert (
        request_id: str,
        url: str,
        time_cost: str,
        origin_input: str,
        real_input: str,
        response: str,
        extra_info: str
    ) -> None:
        DB.fp.db() \
            .table('request') \
            .row() \
            .field('request_id', request_id) \
            .field('url', url) \
            .field('time_cost', time_cost) \
            .field('origin_input', origin_input) \
            .field('real_input', real_input) \
            .field('response', response) \
            .field('extra_info', extra_info) \
            .insert()
        
    @staticmethod
    def request__update_time(request_id: str, time_cost: str) -> None:
        DB.fp.db() \
            .table('request') \
            .row() \
            .field('time_cost', time_cost) \
            .where(f"request_id = '{request_id}'") \
            .update()

    @staticmethod
    def fish__search (
            fuzzys: str = None,
            value: str = None,
            description: str = None,
            identity: str = None,
            type: list[str] = None,
            tags: list[str] = None,
            is_marked: int = None,
            is_locked: int = None,
            page_num: int = None,
            page_size: int = None,
        ) -> tuple[int, list[Fish]]:
        condition = '1=1'
        if fuzzys != None:
            condition += f" and (value like '%{fuzzys}%' or description like '%{fuzzys}%')"
        if value != None:
            condition += f" and (value = '{value}')"
        if description != None:
            condition += f" and (description = '{description}')"
        if identity != None:
            condition += f" and (identity = '{identity}')"
        if type != None:
            keyword = "'" + "','".join(type) + "'"
            condition += f" and (type in ({keyword}))"
        if tags != None:
            keyword = f"%{'%'.join(tags)}%"
            condition += f" and (tags like '{keyword}')"
        if is_marked != None:
            condition += f" and (is_marked = {is_marked})"
        if is_locked != None:
            condition += f" and (is_locked = {is_locked})"
        extra = 'order by update_time desc'
        if page_size != None:
            extra += f" limit {page_size}"
        if page_num != None:
            extra += f" offset {page_size * (page_num-1)}"
        cnt = DB.fp.db() \
            .table('fish') \
            .cols('count(*)') \
            .where(condition) \
            .select(print_sql=True)[0][0]
        fish = DB.fp.db() \
            .table('fish') \
            .where(condition) \
            .extra(extra) \
            .select(print_sql=True)
        return cnt, Fish.from_rows(fish)

    @staticmethod
    def fish__pick(id: int) -> list[Fish]:
        res = DB.fp.db() \
            .table('fish') \
            .where(f"id={id}") \
            .select(print_sql=True)
        return Fish.from_rows(res)
    
    @staticmethod
    def fish__exist(identity: str) -> bool:
        res = DB.fp.db().execute(f"select count(*) from fish where identity='{identity}';", print_sql=True)
        return res[0][0] > 0
    
    @staticmethod
    def fish__insert (
            value: bytes,
            description: str,
            identity: str,
            type: str,
            tags: str,
            extra_info: str,
        ) -> None:
        DB.fp.db() \
            .table('fish') \
            .row() \
            .field('value', ..., value) \
            .field('description', description) \
            .field('identity', identity) \
            .field('type', type) \
            .field('tags', tags) \
            .field('extra_info', extra_info) \
            .insert(print_sql=True)
        
    @staticmethod
    def fish__update (
            id: int,
            value: bytes = None,
            description: str = None,
            identity: str = None,
            type: str = None,
            tags: str = None,
            is_marked: int = None,
            is_locked: int = None,
            extra_info: str = None,
        ) -> None:
        DB.fp.db() \
            .table('fish') \
            .row() \
            .field('value', ..., value) \
            .field('description', description) \
            .field('identity', identity) \
            .field('type', type) \
            .field('tags', tags) \
            .field('is_marked', is_marked) \
            .field('is_locked', is_locked) \
            .field('extra_info', extra_info) \
            .where(f'id={id}') \
            .update(print_sql=True)
        
    @staticmethod
    def fish__delete(id: int) -> None:
        DB.fp.db().table('fish').where(f'id={id}').delete(print_sql=True)
