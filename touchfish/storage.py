from .config import Config
from .definition import *
from yfunc import *
import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
# from whoosh.query import Term, Prefix, FuzzyTerm
from whoosh.qparser import QueryParser
from loguru import logger

class DataBase:

    init_sql = [
        """
            drop table if exists fish;
        """,
        """
            create table fish (
                id integer PRIMARY KEY AUTOINCREMENT,
                identity varchar(64) NOT NULL,
                type varchar(16) NOT NULL,
                byte_count integer NOT NULL,
                preview blob DEFAULT NULL,
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

    # todo: yfunc.ystr.db: select return dict

    @staticmethod
    def fish__parse_row(row: tuple) -> FishResp:
        return FishResp(
            id = row[0],
            identity = row[1],
            type = row[2],
            byte_count=row[3],
            preview=None,
            description = row[4],
            tags = str_parse_tags(row[5]),
            is_marked = True if row[6] == 1 else False,
            is_locked = True if row[7] == 1 else False,
            extra_info = row[8], 
            create_time = row[9], 
            update_time = row[10],
        )
    
    @staticmethod
    def fish__parse_rows(rows: list[tuple]) -> list['FishResp']:
        res = []
        for row in rows:
            try:
                res.append(DataBase.fish__parse_row(row))
            except Exception as e:
                logger.warning(f'parse db row to fish - ignore a row: parse failed, row_id={row[0] if len(row)>0 else -1}', e)
        return res

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
            value_identity: list[str] = None,
            identity: list[str] = None,
            type: list[str] = None,
            tags: list[str] = None,
            is_marked: int = None,
            is_locked: int = None,
            page_num: int = None,
            page_size: int = None,
        ) -> tuple[int, list[FishResp]]:
        condition = '1=1'
        if description != None and value_identity != None:
            keyword = "'" + "','".join(value_identity) + "'"
            condition += f" and (description like '%{description}%' or identity in ({keyword}))"
        if description != None and value_identity == None:
            condition += f" and (description like '%{description}%')"
        if value_identity != None and description == None:
            keyword = "'" + "','".join(value_identity) + "'"
            condition += f" and (identity in ({keyword}))"
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
            .select(sql_printer=logger)[0][0]
        fish = ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .cols(
                'id', 'identity', 'type', 'byte_count', 
                'description', 'tags', 'is_marked', 'is_locked',
                'extra_info', 'create_time', 'update_time',
            ) \
            .where(condition) \
            .extra(extra) \
            .select(sql_printer=logger)
        return cnt, DataBase.fish__parse_rows(fish)
    
    @staticmethod
    def fish__exist(identity: str) -> bool:
        res = ystr(Config.path__db).filepath().db().execute(f"select count(*) from fish where identity='{identity}';", sql_printer=logger)
        return res[0][0] > 0
    
    @staticmethod
    def fish__insert (
            identity: str,
            type: str,
            byte_count: int,
            preview: bytes,
            description: str,
            tags: str,
            is_marked: bool,
            is_locked: bool,
            extra_info: str,
        ) -> None:
        ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .row() \
            .field('identity', identity) \
            .field('type', type) \
            .field('byte_count', byte_count) \
            .field('preview', ..., preview) \
            .field('description', description) \
            .field('tags', tags) \
            .field('is_marked', 1 if is_marked else 0) \
            .field('is_locked', 1 if is_locked else 0) \
            .field('extra_info', extra_info) \
            .insert(sql_printer=logger)
        
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
            .update(sql_printer=logger)
        
    @staticmethod
    def fish__delete(id: int) -> None:
        ystr(Config.path__db).filepath().db().table('fish').where(f'id={id}').delete(sql_printer=logger)

    @staticmethod
    def fish__delete_list(ids: list[int]) -> None:
        if len(ids) == 0:
            return
        ids = [str(id) for id in ids]
        ystr(Config.path__db).filepath().db().table('fish').where(f'id in ({','.join(ids)})').delete(sql_printer=logger)

    @staticmethod
    def fish__select_preview(identity: str) -> bytes | None:
        res = ystr(Config.path__db).filepath().db() \
            .table('fish') \
            .cols('preview') \
            .where(f"identity='{identity}'") \
            .select(sql_printer=logger)
        if len(res) > 0:
            return res[0][0]
        return None        

class FishIndex:

    schema = Schema (
        identity = ID(unique=True, stored=True),
        value = TEXT(),
    )

    idx: index.FileIndex = None
    
    def open_index() -> None:
        FishIndex.idx = index.open_dir(Config.path__fishindex)
    
    def create_index() -> None:
        index.create_in(Config.path__fishindex, FishIndex.schema)

    def add_document(identity: str, value: str) -> None:
        writer = FishIndex.idx.writer()
        try:
            writer.add_document(identity=identity, value=value)
            writer.commit()
        except:
            writer.cancel()
            raise

    def remove_document(identity: str) -> None:
        writer = FishIndex.idx.writer()
        try:
            writer.delete_by_term("identity", identity)
            writer.commit()
        except:
            writer.cancel()
            raise

    def search_document(keyword: str) -> list[str]:
        qp = QueryParser("value", schema=FishIndex.schema)
        q = qp.parse(f'*{keyword}*')
        with FishIndex.idx.searcher() as searcher:
            results = searcher.search(q)
            identity_hits = [result['identity'] for result in results]
        return ylist(identity_hits).unique()

    def build_index():
        pass

class FileSystem:

    fishdata_url_cache: dict[str, str] = {}

    def update_cache() -> None:
        new_cache = {}
        for url in FileSystem.fishdata__urls():
            filename = os.path.basename(url)
            try:
                identity = filename.split('_')[0]
                if identity in new_cache:
                    logger.warning(f'duplicated identity of fishdata: {new_cache[identity]} and {url}')
                else:
                    new_cache[identity] = url
            except:
                logger.warning(f'fishdata file ignored, filename invalid: {url}')
        FileSystem.fishdata_url_cache = new_cache

    def fishdata__urls() -> list[str]:
        return ystr(Config.path__fishdata__active).filepath().search()

    def fishdata__save(value: bytes, type: FishType) -> None:
        identity = ybytes(value).md5() # duplicate calculate
        fishdata_filename = f'{identity}_{type.name}_{ystr().timestamp().now()}'
        ybytes(value).to_file(os.path.join(Config.path__fishdata__active, fishdata_filename))
        FileSystem.update_cache()

    def fishdata__expire(identity: str) -> None:
        for url in FileSystem.fishdata__urls():
            filename = os.path.basename(url)
            if filename.startswith(identity):
                os.rename(url, os.path.join(Config.path__fishdata__expired, filename))
        FileSystem.update_cache()

    def fishdata__read(identity: str) -> bytes | None:
        if identity == None:
            return None
        if identity in FileSystem.fishdata_url_cache:
            return ybytes.from_file(FileSystem.fishdata_url_cache[identity])
        return None
