from yfunc import *
from config import Config
from definition import FishIndex


class DB:

    init_sql = [
        """
            drop table if exists fish;
        """,
        """
            create table fish (
            id integer PRIMARY KEY AUTOINCREMENT,
            identity varchar(64) NOT NULL,
            type varchar(16) NOT NULL,
            description text NOT NULL DEFAULT '',
            tags varchar(128) NOT NULL DEFAULT '',
            is_marked tinyint NOT NUll DEFAULT 0,
            is_locked tinyint NOT NUll DEFAULT 0,
            extra_info text NOT NULL DEFAULT '{}',
            create_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime')),
            update_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime')),
            CONSTRAINT unique_data UNIQUE (identity)
            );
        """,
        """
            create index index_time on fish (update_time);
        """,
        """
            drop TRIGGER if exists update_fish;
        """,
        """
            CREATE TRIGGER update_fish
            AFTER UPDATE ON fish
            FOR EACH ROW
            BEGIN
                UPDATE fish SET update_time = datetime(CURRENT_TIMESTAMP, 'localtime') WHERE id = NEW.id;
            END;
        """,
        """
            drop table if exists request;
        """,
        """
            create table request (
            id integer PRIMARY KEY AUTOINCREMENT,
            request_id varchar(64),
            url varchar(64),
            time_cost text,
            origin_input text,
            real_input text,
            response text,
            extra_info text,
            create_time DATETIME NOT NULL DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime'))
        );
        """,
    ]

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
        ystr(Config.path__db).filepath().db() \
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
        ystr(Config.path__db).filepath().db() \
            .table('request') \
            .row() \
            .field('time_cost', time_cost) \
            .where(f"request_id = '{request_id}'") \
            .update()

    @staticmethod
    def fish__search (
            description: str = None,
            identity: list[str] = None,
            type: list[str] = None,
            tags: list[str] = None,
            is_marked: int = None,
            is_locked: int = None,
            page_num: int = None,
            page_size: int = None,
        ) -> tuple[int, list[FishIndex]]:
        condition = '1=1'
        if description != None:
            condition += f" and (description like '%{description}%')"
        if identity != None:
            keyword = "'" + "','".join(identity) + "'"
            condition += f" and (identity in ({keyword}))"
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
        cnt = ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .cols('count(*)') \
            .where(condition) \
            .select(print_sql=True)[0][0]
        fish = ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .where(condition) \
            .extra(extra) \
            .select(print_sql=True)
        return cnt, FishIndex.from_rows(fish)

    @staticmethod
    def fish__pick(id: int) -> list[FishIndex]:
        res = ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .where(f"id={id}") \
            .select(print_sql=True)
        return FishIndex.from_rows(res)
    
    @staticmethod
    def fish__exist(identity: str) -> bool:
        res = ystr(Config.path__db).filepath().db().execute(f"select count(*) from fish where identity='{identity}';", print_sql=True)
        return res[0][0] > 0
    
    @staticmethod
    def fish__insert (
            identity: str,
            type: str,
            description: str,
            tags: str,
            extra_info: str,
        ) -> None:
        ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .row() \
            .field('identity', identity) \
            .field('type', type) \
            .field('description', description) \
            .field('tags', tags) \
            .field('extra_info', extra_info) \
            .insert(print_sql=True)
        
    @staticmethod
    def fish__update (
            id: int,
            identity: str = None,
            type: str = None,
            description: str = None,
            tags: str = None,
            is_marked: int = None,
            is_locked: int = None,
            extra_info: str = None,
        ) -> None:
        ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .row() \
            .field('type', type) \
            .field('description', description) \
            .field('identity', identity) \
            .field('tags', tags) \
            .field('is_marked', is_marked) \
            .field('is_locked', is_locked) \
            .field('extra_info', extra_info) \
            .where(f'id={id}') \
            .update(print_sql=True)
        
    @staticmethod
    def fish__delete(id: int) -> None:
        ystr(Config.path__db).filepath().db().table('fish').where(f'id={id}').delete(print_sql=True)

