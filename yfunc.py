from typing import *
import os
from io import BytesIO
import time
import math
import itertools as its
import functools as fts
import re
import json as js
import hashlib
import clipboard
import random
from PIL import Image
import sqlite3
import zipfile
import uuid
from loguru import logger

#------------------------

class ybytes(bytes):
    
    @staticmethod
    def from_file(filepath: str) -> 'ybytes':
        with open(filepath, 'rb') as f:
            content = f.read()
        return ybytes(content)
    
    def to_file(self, filepath: str):
        with open(filepath, 'wb') as f:
            f.write(self)

    @staticmethod
    def from_str(s: str, encode='utf-8') -> 'ybytes':
        return ybytes(s.encode(encoding=encode))
    
    def to_str(self, encode='utf-8') -> 'ystr':
        return ystr(self.decode(encoding=encode))
    
    def desc(self) -> 'ystr':
        try:
            return self.to_str()
        except:
            return ystr(self.__str__()) 
    
    def size(self, unit=None, n=2) -> 'ystr':
        B_count = len(self)
        if ystr(unit).of('B'):
            return f'{round(B_count, n)}B'
        if ystr(unit).of('KB'):
            return f'{round(B_count/1024, n)}KB'
        if ystr(unit).of('MB'):
            return f'{round(B_count/(1024*1024), n)}MB'
        if ystr(unit).of('GB'):
            return f'{round(B_count/(1024*1024*1024), n)}GB'
        if B_count < 1024:
            return f'{round(B_count, n)}B'
        KB_count = B_count / 1024
        if KB_count < 1024:
            return f'{round(KB_count, n)}KB'
        MB_count = KB_count / 1024
        if MB_count < 1024:
            return f'{round(MB_count, n)}MB'
        GB_count = MB_count / 1024
        return f'{round(GB_count, n)}GB'
    
    @staticmethod
    def compress(output_path: str, *filepath: str):
        if ystr(output_path).filepath().exist():
            raise Exception("output_path exists")
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as f:
            for file in filepath:
                f.write(file)

    @staticmethod
    def extract(zip_file: str, output_dir: str):
        with zipfile.ZipFile(zip_file, 'r') as f:
            f.extractall(output_dir)

    def md5(self) -> 'ystr':
        return ystr(hashlib.md5(self).hexdigest())
    
    def __str__(self):
        return f'<bytes: {self.size()}>'
    
    def __repr__(self):
        return f'<bytes: {self.size()}>'
    
#------------------------

class ystr(str):

    re_pattern_cache: dict = {}
    time_count = 0

    ##-----------------------

    def __add__(self, __val) -> 'ystr':
        return ystr(super().__add__(__val))

    def __getitem__(self, __key) -> 'ystr':
        return ystr(super().__getitem__(__key))
    
    ##-----------------------

    def datetime(self) -> 'datetime':
        return datetime(self)

    def filepath(self) -> 'filepath':
        return filepath(self)

    def java(self) -> 'java':
        return java(self)

    def json(self) -> 'json':
        return json(self)

    def mathematics(self) -> 'mathematics':
        return mathematics(self)

    def number(self) -> 'number':
        return number(self)

    def row(self) -> 'row':
        return row(self)

    def sql(self) -> 'sql':
        return sql(self)

    def text(self) -> 'text':
        return text(self)

    def timestamp(self) -> 'timestamp':
        return timestamp(self)

    def timedelta(self) -> 'timedelta':
        return timedelta(self)

    def url(self) -> 'url':
        return url(self)

    def variable(self) -> 'variable':
        return variable(self)

    def word(self) -> 'word':
        return word(self)

    ##-----------------------
    
    def count_time(self, flag=None) -> 'ystr':
        t = int(time.time()*1000)
        if flag != None:
            print(f'{flag}: {t-ystr.time_count} ms')
        ystr.time_count = t
        return self

    def print(self) -> 'ystr':
        print('--------------------BEGIN--------------------')
        print(self)
        print('---------------------END---------------------')
        return self

    @staticmethod
    def from_file(path: str, encode='utf-8') -> 'ystr':
        with open(path, 'r', encoding=encode) as f:
            content = f.read()
        return ystr(content)
    
    def to_file(self, path: str, encode='utf-8', force=False) -> 'ystr':
        if not force and not ystr(path).filepath().exist():
            raise Exception('path not exists, use force=True to create path')
        if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding=encode) as f:
            f.write(self)
        return self

    @staticmethod
    def from_clipboard() -> 'ystr':
        return ystr(clipboard.paste())

    def to_clipboard(self) -> 'ystr':
        clipboard.copy(self)
        return self

    def appendto_clipboard(self, spacing='') -> 'ystr':
        old = clipboard.paste()
        clipboard.copy(old+spacing+self)
        return self

    def split(self, by: str = None, trim_each=False, remove_null=False) -> list['ystr']:
        return [
                ystr(s.strip() if trim_each else s) 
                for s in super().split(by)
                if not remove_null or s != ''
            ]

    def strip(self, t: str = None) -> 'ystr':
        return ystr(super().strip(t))
    
    def join(self, ss: Iterable[str]) -> 'ystr':
        return ystr(super().join(ss))

    def replace(self, t: str, by: str, limit=-1) -> 'ystr':
        return ystr(super().replace(t, by, limit))

    def to_rows(self) -> list['ystr']:
        return self.split('\n', trim_each=True, remove_null=True)
    
    def to_words(self) -> list['ystr']:
        return self.split(trim_each=True, remove_null=True)

    def shrink(self, spacing='') -> 'ystr':
        return ystr(spacing).join(self.to_rows())

    @staticmethod
    def do_re_action_with_cache(action: str, r: str, s: str):
        if r in ystr.re_pattern_cache:
            pt = ystr.re_pattern_cache[r]
        else:
            pt = re.compile(r)
            # print('do complie:' + r)
            ystr.re_pattern_cache[r] = pt
        if action == 'match':
            return pt.match(s)
        if action == 'search':
            return pt.search(s)
        if action == 'findall':
            return pt.findall(s)

    def re_match(self, r: str) -> tuple['ystr', int, int]:
        if r == None:
            return ystr(), -1, -1
        # mt = re.match(r, self)
        mt = ystr.do_re_action_with_cache('match', r, self)
        if mt == None:
            return ystr(), -1, -1
        return ystr(mt.group()), mt.start(), mt.end()

    def re_search(self, r: str) -> tuple['ystr', int, int]:
        if r == None:
            return ystr(), -1, -1
        # mt = re.search(r, self)
        mt = ystr.do_re_action_with_cache('search', r, self)
        if mt == None:
            return ystr(), -1, -1
        return ystr(mt.group()), mt.start(), mt.end()

    def re_findall(self, r: str) -> list['ystr']:
        if r == None:
            return []
        # return [ystr(s) for s in re.findall(r, self)]
        return [ystr(s) for s in ystr.do_re_action_with_cache('findall', r, self)]

    def is_match(self, r: str) -> bool:
        return self.re_match(r)[1] != -1 and self.re_match(r)[0] == self
    
    def any_match(self, *r) -> bool:
        return any(self.is_match(rr) for rr in r)

    def of(self, *s: str, r=None, ignore_case=True) -> bool:
        rs = ylist(s).collect(ystr)
        if ignore_case:
            rs = ['(?i)'+r for r in rs]
        if r != None:
            rs.append(r)
        return self.any_match(*rs)
    
    # 寻找一些模式串t, 返回所有t的位置[l, r)的生成器
    # 如果reverse为True, 则从右往左找, 否则从左往右找
    # 如果两个模式串前后冲突, 则按找的顺序取第一个
    # 如果没有任何模式串, 返回 (-1, -1)
    def finds(self, *t: str, reverse=False) -> Generator[tuple[int, int], None, None]:
        n = len(self)
        k = -1 if reverse else n
        bound = n - k
        exist = False
        while True:
            pos = k, k
            for p in (p for p in t if len(p) > 0):
                cur = self.rfind(p, 0, bound) if reverse else self.find(p, bound)
                if cur == -1:
                    continue
                if (reverse and cur > pos[0]) or (not reverse and cur < pos[0]):
                    pos = cur, cur+len(p)
            if pos[0] == k:
                break
            exist = True
            bound = pos[int(k>=0)]
            yield pos
        if not exist:
            yield -1, -1
    
    # 返回第一个模式串t的位置[l, r)
    # 如果没找到, 返回 (-1, -1)
    def find_first(self, t: str) -> tuple[int, int]:
        return next(self.finds(t))

    # 返回最后一个模式串t的位置[l, r)
    # 如果没找到, 返回 (-1, -1)
    def find_last(self, t: str) -> tuple[int, int]:
        return next(self.finds(t, reverse=True))

    # 返回在第一个after之后, 第一个before之前的第一个l和第一个r之间的子串
    # 如果r为None, 默认等于l
    # 如果reverse为True, 则从右往左找, 否则从左往右找
    # 如果没找到, 返回空串
    def find_around(self, l: str, r: str = None, after: str = None, before: str = None, reverse=False) -> 'ystr':
        poses = self.finds(*ylist([after, before, l, r]).collect(ystr).unique(), reverse=reverse)
        if r == None:
            r = l
        res = ''
        if reverse:
            step = 0 if before != None else 1
            res_x, res_y = -1, -1
            for x, y in poses:
                cur = self[x:y]
                if step == 0 and cur == before:
                    step = 1
                    continue
                if step > 0 and cur == after:
                    break
                if step == 1 and cur == r:
                    res_y = x
                    step = 2
                    continue
                if step == 2 and cur == l:
                    res_x = y
                    break
            res = self[res_x:res_y] if res_x != -1 and res_y != -1 else ''
        else:
            step = 0 if after != None else 1
            res_x, res_y = -1, -1
            for x, y in poses:
                cur = self[x:y]
                if step == 0 and cur == after:
                    step = 1
                    continue
                if step > 0 and cur == before:
                    break
                if step == 1 and cur == l:
                    res_x = y
                    step = 2
                    continue
                if step == 2 and cur == r:
                    res_y = x
                    break
            res = self[res_x:res_y] if res_x != -1 and res_y != -1 else ''
        return ystr(res)

    # 按照括号闭合的原则, 找到每一个l对应的r, 返回它们的起始下标映射(key: l_begin_pos, value: r_begin_pos)
    # 如果reverse为True, 则从右往左找, 否则从左往右找
    def close_find(self, l: str, r: str, reverse=False) -> dict[int, int]:
        res = {}
        l_pos_s = []
        for x, y in self.finds(l, r, reverse=reverse):
            if self[x:y] == l:
                l_pos_s.append(x)
            if self[x:y] == r and len(l_pos_s) > 0:
                res[l_pos_s.pop()] = x
        return res

    # 将位置为pos: [l, r)的一些子串去掉后, 返回剩余的每段子串的生成器
    # 如果keep为True, 则也返回去掉的那些子串, 否则丢弃
    # 如果reverse为True, 则从右往左找, 否则从左往右找
    def mult_cut(self, *pos: tuple[int, int], keep=True, reverse=False) -> Generator['ystr', None, None]:
        if len(self) == 0:
            yield ystr()
            return
        ps = [p for p in pos if p[0] <= p[1]]
        if reverse:
            ps.sort(key=lambda x: x[1], reverse=True)
            poses = [(len(self), len(self))]
            for x, y in ps:
                if y <= poses[-1][0]:
                    poses.append((x, y))
        else:
            ps.sort(key=lambda x: x[0])
            poses = [(-1, -1)]
            for x, y in ps:
                if x >= poses[-1][1]:
                    poses.append((x, y))
        poses = poses[1:]
        if len(poses) == 0:
            yield self
            return
        if reverse:
            if len(t:=self[poses[0][1]:])>0: yield t
            for i in range(len(poses)-1):
                if keep and len(t:=self[poses[i][0]:poses[i][1]])>0: yield t
                if len(t:=self[poses[i+1][1]:poses[i][0]])>0: yield t
            if keep and len(t:=self[poses[-1][0]:poses[-1][1]])>0: yield t
            if len(t:=self[:poses[-1][0]])>0: yield t
        else:
            if len(t:=self[:poses[0][0]])>0: yield t
            for i in range(len(poses)-1):
                if keep and len(t:=self[poses[i][0]:poses[i][1]])>0: yield t
                if len(t:=self[poses[i][1]:poses[i+1][0]])>0: yield t
            if keep and len(t:=self[poses[-1][0]:poses[-1][1]])>0: yield t
            if len(t:=self[poses[-1][1]:])>0: yield t

    # 按一系列模式串t分割, 返回分割后的每段子串的生成器
    # 如果keep为True, 则也返回去掉的那些子串, 否则丢弃
    # 如果reverse为True, 则从右往左找, 否则从左往右找
    def cuts(self, *t: str, keep=True, reverse=False) -> Generator['ystr', None, None]:
        poses = list(self.finds(*t, reverse=reverse))
        return self.mult_cut(*poses, keep=keep, reverse=reverse)
    
    # 将下标为index的一些字符去掉后, 返回剩余的每段子串的生成器
    # 如果keep为True, 则也返回去掉的那些子串, 否则丢弃
    def cut(self, *index: int, keep=True) -> Generator['ystr', None, None]:
        poses = [(i, i+1) for i in index if i >= 0 and i < len(self)]
        return self.mult_cut(*poses, keep=keep)

    def discard(self, *pos: tuple[int, int], reverse=False) -> 'ystr':
        return ystr().join(self.mult_cut(*pos, keep=False, reverse=reverse))

    # 按第一个l和最后一个r分割, 返回三段子串(不保留l和r)
    def lr_split(self, l: str = ' ', r: str = ' ') -> tuple['ystr', 'ystr', 'ystr']:
        x1, y1 = self.find_first(l)
        x2, y2 = self.find_last(r)
        if x1 == -1 and x2 == -1:
            return ystr(), self, ystr()
        if x1 == -1:
            return ystr(), self[:x2], self[y2:]
        if x2 == -1:
            return self[:x1], self[y1:], ystr()
        return self[:x1], self[y1:x2], self[y2:]

    # 根据by进行split但忽略brackets中的by
    def close_split(
            self, by: str = ' ', 
            brackets: tuple[tuple[str, str]] = (('(',')'),('[',']'),('<','>'),('{','}'),('"','"'),("'","'"),('`', '`')),
            trim_each: bool = True,
            remove_null: bool = True,
        ) -> Generator['ystr', None, None]:
        parts = self.cuts(by, *ylist(brackets).flatten())
        cur = ''
        balance = [0 for _ in brackets]
        for p in parts:
            if p == by and all(x==0 for x in balance):
                if trim_each:
                    cur = cur.strip()
                if cur != '' or not remove_null:
                    yield ystr(cur)
                cur = ''
                continue
            for i, cl in enumerate(brackets):
                if cl[0] != cl[1]:
                    if p == cl[0]:
                        balance[i] += 1
                    if p == cl[1]:
                        balance[i] -= 1
                else:
                    if p == cl[0]:
                        balance[i] ^= 1
            cur += p
        if all(x==0 for x in balance):
            if trim_each:
                cur = cur.strip()
            if cur != '' or not remove_null:
                yield ystr(cur)       

    def md5(self, encode='utf-8') -> 'ystr':
        return ybytes.from_str(self, encode=encode).md5()
    
    @staticmethod
    def uuid() -> 'ystr':
        return ystr(uuid.uuid4())

class row():
    
    def __init__(self, s: str) -> None:
        self.s = ystr(s)
    
    @staticmethod
    def from_words(*word: str) -> 'ystr':
        return ystr(' '.join(word))

class word():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

class variable():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def format(self, style: str) -> 'ystr':
        if self.s == '' or len(style) < 4:
            return self.s
        def split_to_words(s: ystr) -> list['ystr']:
            if '_' in s:
                return s.split('_')
            ret = []
            cur = ''
            for c in s:
                if c.islower():
                    cur += c
                else:
                    if cur != '':
                        ret.append(cur)
                    cur = c
            if cur != '':
                ret.append(cur)
            return ret
        words = [word.lower() for word in split_to_words(self.s)]
        res_words = []
        first_word = (words[0][0].lower() if style[0].islower() else words[0][0].upper()) + \
            (words[0][1:].lower() if style[1].islower() else words[0][1:].upper())
        res_words.append(first_word)
        for word in words[1:]:
            cur_word = (word[0].lower() if style[2].islower() else word[0].upper()) + \
                (word[1:].lower() if style[3].islower() else word[1:].upper())
            res_words.append(cur_word)
        return (style[4] if len(style) >= 5 else '').join(res_words)

    def aaBb(self) -> 'ystr':
        return self.format('aaBb')

    def AaBb(self) -> 'ystr':
        return self.format('AaBb')

class datetime():

    def __init__(self, s: str, fmt='%Y-%m-%d %H:%M:%S') -> None:
        self.s = ystr(s)
        self.time_struct = time.strptime(self.s, fmt) if len(s) > 0 else None

    def to_timestamp(self) -> 'ystr':
        if self.time_struct == None:
            return ystr('0000000000')
        return ystr(int(time.mktime(self.time_struct)))
    
    @staticmethod
    def now(onlydate=False) -> 'ystr':
        if onlydate:
            return ystr().timestamp().now().timestamp().to_datetime(fmt='%Y-%m-%d')    
        return ystr().timestamp().now().timestamp().to_datetime()
    
    def weekday(self) -> int:
        if self.time_struct == None:
            return 0
        return self.time_struct.tm_wday + 1
    
    def yearday(self) -> int:
        if self.time_struct == None:
            return 0
        return self.time_struct.tm_yday
    
    def delta(self, dt: str) -> 'ystr':
        delta_second = self.to_timestamp().timestamp().delta(ystr(dt).datetime().to_timestamp())
        return ystr().timedelta().from_second(int(delta_second)).s
    
    def plus(self, td: str) -> 'ystr':
        return self.to_timestamp().timestamp().plus(ystr(td).timedelta().to_second()).timestamp().to_datetime()

class timestamp():

    # 只处理到秒
    def __init__(self, s: str, format=False) -> None:
        self.s = ystr(s).number().format(10) if format else ystr(s)

    @staticmethod
    def now() -> 'ystr':
        return ystr(int(time.time()))

    def to_datetime(self, fmt="%Y-%m-%d %H:%M:%S") -> 'ystr':
        t = time.localtime(int(self.s[:10]))
        return ystr(time.strftime(fmt, t))
    
    def plus(self, second: int) -> 'ystr':
        return self.s.number().calculate('+'+str(second))
    
    def delta(self, ts: ystr) -> 'ystr':
        return self.s.number().calculate('-'+ts)

class timedelta():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)
    
    @staticmethod
    def from_second(second: int) -> 'timedelta':
        flag = '-' if second < 0 else ''            
        second = abs(second)
        m, s = second // 60, second % 60
        h, m = m // 60, m % 60
        d, h = h // 24, h % 24
        return timedelta(f'{flag}{d}d{h}h{m}m{s}s')
    
    def to_second(self) -> int:
        d, h, m, s = self.s.re_findall('\d+')
        return (((int(d)*24+int(h))*60+int(m))*60+int(s))*(-1 if self.s[0]=='-' else 1)

class filepath():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def search(self, *suffix: str) -> list['ystr']:
        def add_check_suffix(res: list['ystr'], path: 'ystr') -> None:
            if suffix == () or any(path.endswith(suff) for suff in suffix if suff != None):
                res.append(path)
        def dfs_search(p: 'ystr') -> list['ystr']:
            ret = []
            if not os.path.isdir(p):
                add_check_suffix(ret, p)
                return ret
            pathes = os.listdir(p)
            for path in pathes:
                full_path = ystr(os.path.join(p, path))
                if os.path.isdir(full_path):
                    ret += dfs_search(full_path)
                else:
                    add_check_suffix(ret, full_path)
            return ret
        return dfs_search(self.s)
    
    def suffix(self, keep_ext=True) -> 'ystr':
        if keep_ext:
            return self.s.split('/')[-1]
        return '.'.join((self.s.split('/')[-1]).split('.')[:-1])
    
    def ext(self) -> 'ystr':
        if os.path.isdir(self.s):
            return ''
        return (self.s.split('/')[-1]).split('.')[-1]

    def exist(self) -> bool:
        return os.path.exists(self.s)

    def txt(self, encode='utf-8') -> 'TextFileHandler':
        return TextFileHandler(self.s, encode)
    
    def db(self, auto_commit=True, auto_close=True, check_same_thread=True) -> 'DBFileHandler':
        return DBFileHandler(self.s, auto_commit=auto_commit, auto_close=auto_close, check_same_thread=check_same_thread)
        
class TextFileHandler:
    
    def __init__(self, path: str, encode='utf-8') -> None:
        self.path = path
        self.content = ystr().from_file(path, encode=encode)
        self.length = len(self.content)
        self.md5 = self.content.md5()

    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

class DBFileHandler:

    def __init__(self, path, auto_commit=True, auto_close=True, check_same_thread=True) -> None:
        self.path = path
        self.auto_commit = auto_commit
        self.auto_close = auto_close
        self.con = sqlite3.connect(path, check_same_thread=check_same_thread)
        self.cr = self.con.cursor()

    def execute(self, sql: str, para=(), auto_commit=None, auto_close=None, print_sql=False) -> 'ylist':
        if print_sql:
            logger.info(f'excute sql: {sql} para count: {len(para)}')
        try:
            res = self.cr.execute(sql, para).fetchall()
        except Exception as e:
            e.add_note(f'Note: sql = {sql}')
            raise
        auto_commit = self.auto_commit if auto_commit == None else auto_commit
        auto_close = self.auto_close if auto_close == None else auto_close
        if auto_commit:
            self.commit()
        if auto_close:
            self.close()
        return ylist(res)

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

    def table(self, table_name: str):
        return SimpleSqlExecuter(self, table_name)
    
    def tables(self) -> 'ylist':
        res = self.table('sqlite_master').cols('name').where("type='table'").select().flatten()
        res.remove('sqlite_sequence')
        return res

class SimpleSqlExecuter:

    def __init__(self, dao: DBFileHandler, table_name: str) -> None:
        self.dao = dao
        self.table_name = table_name
        self.sb = SimpleSqlBuilder()
        self.sb.table(table_name)
        self.parameter = []
        self.force = False

    def cols(self, *col: str) -> 'SimpleSqlExecuter':
        self.sb.cols(*col)
        return self
    
    def vals(self, *val) -> 'SimpleSqlExecuter':
        self.sb.vals(*val)
        return self
    
    def row(self) -> 'SimpleSqlExecuter':
        self.sb.cols()
        self.sb.vals()
        return self
        
    def field(self, col: str, val, para=None, add_none=False) -> 'SimpleSqlExecuter':
        if val != ...:
            self.sb.field(col, val, add_none)
            return self
        if para == None and not add_none:
            return self
        self.sb.field(col, val, add_none)
        self.parameter.append(para)
        return self

    def where(self, where_fragment: str) -> 'SimpleSqlExecuter':
        self.sb.where(where_fragment)
        return self
    
    def extra(self, extra_fragment: str) -> 'SimpleSqlExecuter':
        self.sb.extra(extra_fragment)
        return self
    
    def paras(self, *para) -> 'SimpleSqlExecuter':
        self.parameter = list(para)
        return self
    
    def Y(self) -> 'SimpleSqlExecuter':
        self.force = True
        return self
    
    def N(self) -> 'SimpleSqlExecuter':
        self.force = False
        return self
    
    def insert(self, print_sql=False) -> 'ylist':
        self.sb.method('insert')
        sql = self.sb.build()
        return self.dao.execute(sql, para=self.parameter, print_sql=print_sql)

    def update(self, print_sql=False) -> 'ylist':
        self.sb.method('update')
        sql = self.sb.build()
        if self.sb.where_fragment in ('', None) and not self.force:
            raise Exception('no where condition, will update whole table, are you sure? (Y/N)')
        return self.dao.execute(sql, para=self.parameter, print_sql=print_sql)
    
    def delete(self, print_sql=False) -> 'ylist':
        self.sb.method('delete')
        sql = self.sb.build()
        if self.sb.where_fragment in ('', None) and not self.force:
            raise Exception('no where condition, will delete all rows, are you sure? (Y/N)')
        return self.dao.execute(sql, para=self.parameter, print_sql=print_sql)
    
    def select(self, print_sql=False) -> 'ylist':
        self.sb.method('select')
        sql = self.sb.build()
        return self.dao.execute(sql, para=self.parameter, print_sql=print_sql)

    def describe(self) -> 'ystr':
        res = self.dao.execute (
            f"select sql from sqlite_master where name = '{self.table_name}'",
            auto_commit=True, auto_close=False,
        ).flatten()
        if len(res) == 0:
            raise Exception(f'table {self.table_name} not exists')
        table_detail = ystr(res[0]).sql().parse()
        row_count = self.dao.execute (
            f'select count(*) from {self.table_name}',
            auto_commit=True,
        ).flatten()
        table_detail.row_count = row_count[0]
        return ystr().json().from_object(table_detail)
            
class java():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def parse(self):
        try:
            return JavaClass(self.s)
        except:
            try:
                return JavaFunc(self.s)
            except:
                raise
        
class JavaFuncPara:
    
    def __init__(self, para_raw: str = None) -> None:
        self.type = ''
        self.name = ''
        self.extra = ''

        if para_raw == None:
            return
        parts = list(ystr(para_raw).strip().close_split())
        self.name = parts[-1].shrink(' ')
        self.type = parts[-2].shrink(' ')
        if len(parts) > 2:
            self.extra = ''.join(parts[:-2])
    
    def to_code(self) -> 'ystr':
        return f'{self.type} {self.name}'
    
    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

class JavaFunc:

    def __init__(self, func_raw: str = None) -> None:
        self.func_name = ''
        self.access_level = ''
        self.return_type = ''
        self.paras: list[JavaFuncPara] = []
        self.throw = ''
        self.body = '' # 带tab
        self.annotations: list[ystr] = [] # 暂未解析
        self.extra = ''

        if func_raw == None:
            return
        func_raw = ystr(func_raw)
        _, x, _ = func_raw.re_search(r'(public|private|protect)')
        self.extra = func_raw[:x]
        func_head, self.body, _ = func_raw[x:].strip().lr_split('{', '}')
        if func_head == '':
            func_head = self.body
            self.body = ''
        head_prefix, head_paras, self.throw = func_head.strip().lr_split('(', ')')
        self.access_level, self.return_type, self.func_name = head_prefix.strip().lr_split()
        self.paras = [JavaFuncPara(p) for p in head_paras.strip().close_split(',')]

    def to_code(self) -> 'ystr':
        ret = ystr()
        for an in self.annotations:
            ret += an + '\n'
        ret += f'{self.access_level} {self.return_type} {self.func_name}('
        ret += f'{", ".join(p.to_code() for p in self.paras)})'
        if self.throw != '':
            ret += f' throws {self.throw}'
        ret += ' {\n'
        ret += self.body.strip('\n').rstrip()
        ret += '\n}\n'
        return ret
    
    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

    def gen_ut(self, class_type: str = '') -> 'JavaFunc':
        if class_type.endswith('Service'):
            class_type += 'Impl'
        class_name = ystr(class_type).variable().aaBb()
        res = JavaFunc()
        res.annotations.append('@Test')
        res.access_level = 'public'
        res.return_type = 'void'
        res.func_name = f'test{self.func_name.variable().AaBb()}'
        if self.access_level == 'private':
            res.throw = 'NoSuchMethodException'
        body = ''
        if self.access_level == 'private':
            body += f'    Method targetMethod = {class_type}.class.getDeclaredMethod("{self.func_name}",\n'
            def get_reflect_class(type):
                pt = ParaGenTool(type)
                return pt.collection if pt.collection != '' else pt.full_type
            body += '        ' + ', '.join([f'{get_reflect_class(p.type)}.class' for p in self.paras]) + ');\n'
            body += '    targetMethod.setAccessible(true);\n'
        pts = [ParaGenTool(p.type, p.name) for p in self.paras]
        for pt in pts:
            body += pt.gen_new().text().add_tab()
        body += '    try {\n'
        if self.access_level == 'private':
            body += f"        targetMethod.invoke({class_name}, {', '.join([pt.name for pt in pts])});\n"
        else:
            body += f"        {class_name}.{self.func_name}({', '.join([pt.name for pt in pts])});\n"
        body += '        assertTrue(CAN_REACH_HERE);\n'
        body += '    } catch (Exception e) {\n'
        body += '        fail();\n'
        body += '    }'
        res.body = body
        return res

class JavaField:

    def __init__(self, field_raw: str = None) -> None:
        self.name = ''
        self.type = ''
        self.access_level = ''
        self.comment = ''
        self.annotations: list[ystr] = [] # 暂未解析
        self.extra = ''

        if field_raw == None:
            return
        field_raw = ystr(field_raw).shrink()
        fd, l1, r1 = field_raw.re_search(r'(private|public|protect)[\w\W]*;')
        cm, l2, r2 = field_raw.re_search(r'/\*[\w\W]*\*/')
        self.extra = field_raw.discard((l1, r1), (l2, r2))
        self.comment = cm.strip('/*').strip()
        pos__type = 0
        skip_words = ('public', 'private', 'protect', 'static', 'final')
        fws = list(fd.strip(' ;').close_split())
        for i, w in enumerate(fws):
            if not w.of(*skip_words):
                pos__type = i
                break
        self.type = fws[pos__type]
        self.name = fws[pos__type+1]
        self.access_level = fws[0]

    def to_code(self) -> 'ystr':
        res = ystr()
        if self.comment != '':
            res += '/**\n'
            res += f' * {self.comment}\n'
            res += ' */\n'
        for an in self.annotations:
            res += an + '\n'
        res += f'{self.access_level} {self.type} {self.name};\n'
        return res

    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

class JavaClass:
    
    def __init__(self, java_raw: str = None) -> None:
        self.class_name = ''
        self.package = ''
        self.imports: list[ystr] = []
        self.annotations: list[ystr] = []
        self.fields: list[JavaField] = []
        self.functions: list[JavaFunc] = []

        if java_raw == None:
            return
        flag = True
        cache = ystr()
        for row in ystr(java_raw).to_rows():
            if flag:
                if row.startswith('package '):
                    self.package = row.find_around(l=' ', r=';', after='package')
                if row.startswith('import '):
                    self.imports.append(row.find_around(l=' ', r=';', after='import'))
                if row.startswith('@'):
                    self.annotations.append(row)
                if row.startswith('public class '):
                    self.class_name = row.find_around(l=' ', after='class')
                    flag = False
                continue
            cache += row
            if self.contain_field(cache):
                self.fields.append(JavaField(cache))
                cache = ystr()
            if self.contain_func(cache):
                self.functions.append(JavaFunc(cache))
                cache = ystr()

    def contain_field(self, cache: ystr) -> bool:
        return cache.shrink().is_match(r'[\w\W]*(private|public|protect)[^{}]*;')
    
    def contain_func(self, cache: ystr) -> bool:
        if not cache.shrink().is_match(r'[\w\W]*(private|public|protect)[\w\W]*{[\w\W]*}'):
            return False
        pos, _ = cache.find_first('{')
        return pos in cache.close_find('{', '}').keys()
    
    def to_code(self) -> 'ystr':
        res = ystr()
        res += self.package + ';\n\n'
        res += ystr('\n').join(f'import {im};' for im in self.imports) + '\n\n'
        res += ystr('\n').join(self.annotations) + '\n'
        res += f'public {self.class_name} ' + '{\n\n'
        for f in self.fields:
            res += f.to_code().text().add_tab() + '\n'
        for f in self.functions:
            res += f.to_code().text().add_tab() + '\n'
        res += '}'
        return res
    
    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

    def gen_ut(self) -> 'JavaClass':
        res = JavaClass()
        res.package = self.package
        if 'confirm.rpc' in self.package:
            res.imports.append('static com.bytedance.ea.finance.revenue.confirm.rpc.common.util.test.TestUtils.CAN_REACH_HERE')
            res.imports.append('static com.bytedance.ea.finance.revenue.confirm.rpc.common.util.test.TestUtils.deepCopy')
        else:
            res.imports.append('static com.bytedance.revenue.common.util.test.TestUtils.CAN_REACH_HERE')
            res.imports.append('static com.bytedance.revenue.common.util.test.TestUtils.deepCopy')
        res.imports.append('static org.junit.Assert.assertFalse')
        res.imports.append('static org.junit.Assert.assertTrue')
        res.imports.append('static org.junit.Assert.fail')
        res.imports.append('java.lang.reflect.Method')
        res.imports.append('java.util.*')
        res.imports.append('org.junit.Test')
        res.imports.append('org.junit.runner.RunWith')
        res.imports.append('org.mockito.InjectMocks')
        res.imports.append('org.mockito.Mock')
        res.imports.append('org.mockito.Mockito')
        res.imports.append('org.powermock.core.classloader.annotations.PrepareForTest')
        res.imports.append('org.powermock.modules.junit4.PowerMockRunner')
        res.imports += self.imports
        res.annotations.append('@RunWith(PowerMockRunner.class)')
        res.annotations.append('@PrepareForTest({SpringApplicationUtils.class})')
        res.class_name = self.class_name + 'Test'
        tested_bean = JavaField()
        tested_bean.annotations.append('@InjectMocks')
        tested_bean.name = self.class_name.variable().aaBb().replace('Impl', '')
        tested_bean.type = self.class_name
        tested_bean.access_level = 'private'
        res.fields.append(tested_bean)
        for f in self.fields:
            if '@Autowired' in f.extra or '@Resource' in f.extra:
                mocked_bean = JavaField()
                mocked_bean.annotations.append('@Mock')
                mocked_bean.name = f.name
                mocked_bean.type = f.type
                mocked_bean.access_level = 'private'
                res.fields.append(mocked_bean)
        for f in self.functions:
            try:
                res.functions.append(f.gen_ut(self.class_name.replace('Impl', '')))
            except Exception as e:
                e.add_note(f'Note: when gen ut of func {f.func_name}')
                raise
        return res

class ParaGenTool:

    def __init__(self, type: str, name=None) -> None:
        self.full_type = type
        self.collection = ''
        self.warpped = ''
        self.name = name
        
        if type.startswith('List'):
            self.collection = 'List'
            self.warpped = ystr(type).find_around(l='<', r='>')
        if type.startswith('Map'):
            self.collection = 'Map'
            self.warpped = ystr(type).find_around(l='<', r='>')
        if self.name == None:
            self.name = ParaGenTool.name_of_type(type)

    def name_of_type(type: str, id: int = None) -> str:
        id = '' if id == None else str(id)
        if type in ('int', 'Integer', 'long', 'Long'):
            return 'num' + id
        if type == 'String':
            return 'str' + id
        if type in ('boolean', 'Boolean'):
            return 'bool' + id
        if type.startswith('List'):
            warpped = ystr(type).find_around(l='<', r='>')
            return warpped.variable().aaBb() + 'List' + id
        if type.startswith('Map'):
            warpped = ystr(type).find_around(l='<', r='>')
            warpped_types = list(warpped.close_split(','))
            return f'{warpped_types[0].variable().aaBb()}To{warpped_types[1].variable().AaBb()}Map' + id
        return ystr(type).variable().aaBb() + id

    def value_of_type(self, type: str, id: int = None) -> str:
        if type in ('int', 'Integer'):
            return str(1+(0 if id==None else id))
        if type in ('long', 'Long'):
            return str(1+(0 if id==None else id)) + 'L'
        if type == 'String':
            return '"test' + ystr(self.name).variable().AaBb() + (str(id) if id != None else '') + '"'
        if type in ('boolean', 'Boolean'):
            return 'true'
        if type.endswith('Enum'):
            return f'{type}.values()[0]'
        return f'new {type}()'
    
    def gen_list(self, ele_num: int = 0) -> ystr:
        if ele_num == None or ele_num < 0:
            ele_num = 0
        ele_type = self.warpped
        ele_name = self.name if self.collection == '' else ParaGenTool.name_of_type(ele_type)
        list_name = self.name if self.collection == 'List' else (ParaGenTool.name_of_type(ele_type)+'List')
        res = ''
        res += f'List<{ele_type}> {list_name} = new ArrayList<>();\n'
        for i in range(ele_num):
            res += f'{ele_type} {ele_name}{i+1} = {self.value_of_type(ele_type, i)};\n'
            res += f'{list_name}.add({ele_name}{i+1});\n'
        return ystr(res)
    
    def gen_new(self, ele_num: int = 0) -> ystr:
        if ele_num == None or ele_num < 0:
            ele_num = 0
        if self.collection == 'List':
            return self.gen_list(ele_num)
        return ystr(f'{self.full_type} {self.name} = {self.value_of_type(self.full_type)};\n')

class json():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def format(self, indent=4) -> 'ystr':
        return ystr(js.dumps(
                        js.loads(self.s), 
                        ensure_ascii = False, 
                        indent = indent,
                        default = lambda obj: obj.__dict__,
                    )
                )   
    
    @staticmethod
    def from_object(obj, indent=4) -> 'ystr':
        return ystr(js.dumps(
                        obj, 
                        ensure_ascii = False, 
                        indent = indent,
                        default = lambda obj: obj.__dict__,
                    )
                )

    def to_dic(self) -> 'ydic':
        return ydic(js.loads(self.s))

class number():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def format(self, length, fill='0') -> 'ystr':
        if len(self.s) > length:
            return (self.s[-length:])
        return ystr(fill*(length-len(self.s))+self.s)
    
    def calculate(self, s: str) -> 'ystr':
        return (self.s+s).mathematics().calculate()

class mathematics():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    def calculate(self) -> 'ystr':
        return ystr(eval(self.s))

class sql():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

    @staticmethod
    def gen_in(*word: str, row_count=0, add_quotes=False) -> 'ystr':
        words = ["'" + w + "'" for w in word] if add_quotes else word
        try:
            row_count = int(row_count)
        except:
            row_count = 0
        if row_count < 1:
            fra = ','.join(words)
            res = f'in ({fra})'
        else:
            fra = ''
            for i, w in enumerate(words):
                fra += f'{w},\n' if (i+1) % row_count == 0 else f'{w},'
            fra = fra.strip()[:-1]
            res = 'in (\n' + ystr(fra).text().add_tab() + '\n)'
        return ystr(res)

    def parse(self):
        return Table(self.s)

    @staticmethod
    def builder() -> 'SimpleSqlBuilder':
        return SimpleSqlBuilder()

class SimpleSqlBuilder:

    def __init__(self) -> None:
        self.sql_type = ''
        self.table_name = ''
        self.columns: list[list[str]] = []
        self.values: list[list[str]] = []
        self.where_fragment = ''
        self.extra_fragment = ''

    def table(self, table_name: str) -> 'SimpleSqlBuilder':
        self.table_name = table_name
        return self
    
    def cols(self, *col: str) -> 'SimpleSqlBuilder':
        self.columns.append(list(col))
        return self
    
    @staticmethod
    def _parse_(v):
        if v == None:
            return 'NULL'
        if v == ...:
            return '?'
        if isinstance(v, str):
            v = v.replace("'", "''")
            return "'"+v+"'"
        return str(v)

    def vals(self, *vals) -> 'SimpleSqlBuilder':
        self.values.append([SimpleSqlBuilder._parse_(v) for v in vals])
        return self

    def field(self, col: str, val, add_none=False) -> 'SimpleSqlBuilder':
        if val == None and not add_none:
            return
        self.columns[-1].append(col)
        self.values[-1].append(SimpleSqlBuilder._parse_(val))
    
    def method(self, sql_type: str) -> 'SimpleSqlBuilder':
        self.sql_type = sql_type
        return self

    def where(self, where_fragment: str) -> 'SimpleSqlBuilder':
        self.where_fragment = where_fragment
        return self
    
    def extra(self, extra_fragment: str) -> 'SimpleSqlBuilder':
        self.extra_fragment = extra_fragment
        return self

    def build(self) -> 'ystr':
        if self.sql_type == 'insert':
            column_fragment = f"({', '.join(self.columns[0])})" if len(self.columns) > 0 else ''
            insert_fragment = ', '.join(f'({", ".join(val)})' for val in self.values)
            sql = f"insert into {self.table_name} {column_fragment} values {insert_fragment}"
        elif self.sql_type == 'update':
            update_fragment = ', '.join(f'{self.columns[0][i]}={self.values[0][i]}' for i in range(len(self.columns[0])))
            sql = f"update {self.table_name} set {update_fragment}"
            if self.where_fragment != '':
                sql += f" where {self.where_fragment}"
        elif self.sql_type == 'delete':
            sql = f"delete from {self.table_name}"
            if self.where_fragment != '':
                sql += f" where {self.where_fragment}"
        elif self.sql_type == 'select':
            # todo: selected col
            cols_fragment = '*' if self.columns == [] else ', '.join(self.columns[0])
            sql = f"select {cols_fragment} from {self.table_name}"
            if self.where_fragment != '':
                sql += f" where {self.where_fragment}"
        else:
            raise Exception(f'invalid sql type: {self.sql_type}')
        if self.extra_fragment != '':
            sql += ' ' + self.extra_fragment
        sql += ';'
        return ystr(sql)

class Col:

    def __init__(self) -> None:
        self.name = ''
        self.type = ''
        self.comment = ''
        self.can_null = True
        self.default = ''

    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)
    
class Table:

    def __new__(cls, sql: str):
        self = super().__new__(cls)
        self.table_name = ''
        self.cols = []
        self.keys = []
        self.extra = ''
        return self

    def __init__(self, sql: str) -> None:
        sql = ystr(sql)
        x, _ = sql.find_first('(')
        y, _ = sql.find_last(')')
        if x == -1 or y == -1:
            raise 
        part1 = sql[:x]
        part2 = sql[x+1:y]
        part3 = sql[y+1:]
        pw1 = ystr(part1).to_words()
        if not ystr('create').of(*pw1):
            raise 
        for i, w in enumerate(pw1):
            if w.of('table'):
                break
        self.table_name = pw1[i+1].strip(" ;`'")
        self.cols: list[Col] = []
        self.keys = []
        pr2 = part2.close_split(',', remove_null=True, trim_each=True)
        for r in pr2:
            try:
                pw2 = list(r.close_split())
                if ystr('key').of(*pw2):
                    self.keys.append(r)
                    continue
                t = Col()
                t.name = pw2[0].strip(" ;`'")
                t.type = pw2[1].strip(" ;`'")
                for i, w in enumerate(pw2):
                    if i+1 >= len(pw2):
                        break
                    if w.of('not') and pw2[i+1].of('null'):
                        t.can_null = False
                    if w.of('comment'):
                        t.comment = pw2[i+1].strip(" ;`'")
                    if w.of('default'):
                        t.default = pw2[i+1].strip(" ;`'")
                self.cols.append(t)
            except Exception as e:
                e.add_note(f'at:[{r}]')
                raise
        self.extra = part3.strip(' ;')

    def to_json(self) -> 'ystr':
        return ystr().json().from_object(self)

class text():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)
    
    @staticmethod
    def from_rows(*row: 'ystr') -> 'ystr':
        return ystr('\n'.join(row))
    
    def add_tab(self) -> 'ystr':
        poses = [p[0] for p in self.s.finds('\n')]
        res = '    ' + self.s[:poses[-1]].replace('\n', '\n    ') + \
            (t if (t:=self.s[poses[-1]:]).strip()=='' else t.replace('\n', '\n    '))
        return ystr(res)
    
    def pos_to_rid(self, pos: int) -> int:
        if pos < 0 or pos >= len(self.s):
            return -1
        return len(self.s[:pos].re_findall('\n'))
            

class url():

    def __init__(self, s: str) -> None:
        self.s = ystr(s)

#------------------------

class ylist(list):

    def __add__(self, __val) -> 'ylist':
        return ylist(super().__add__(__val))
    
    ##-----------------------

    @staticmethod
    def from_str(s: str, encode='utf-8') -> 'ylist':
        return ylist(ybytes.from_str(s, encode=encode))
    
    def to_str(self, encode='utf-8') -> 'ystr':
        return ybytes(self).to_str(encode=encode)
        
    @staticmethod
    def from_bytes(b: bytes) -> 'ylist':
        return ylist(b)
    
    def to_bytes(self) -> 'ybytes':
        return ybytes(self)

    def print(self) -> 'ylist':
        print('--------------------BEGIN--------------------')
        print(self)
        print('---------------------END---------------------')
        return self
    
    def count(self) -> int:
        return len(self)

    def append(self, obj) -> 'ylist':
        super().append(obj)
        return self

    def inter(self, another_collection) -> 'ylist':
        ret = set()
        for x in self:
            if x in another_collection:
                ret.add(x)
        return ylist(ret)
    
    def unique(self) -> 'ylist':
        return ylist(set(self))
    
    def sort(self, key=None, reverse=False) -> 'ylist':
        super().sort(key=key, reverse=reverse)
        return self
    
    def group(self, size: int = 0) -> 'ylist':
        if size <= 0:
            return self
        res = ylist()
        sub = ylist()
        cnt = 0
        for o in self:
            if cnt == size:
                res.append(sub)
                sub = ylist()
                cnt = 0
            sub.append(o)
            cnt += 1
        if len(sub) > 0:
            res.append(sub)
        return res

    def flatten(self):
        def dfs_flatten(obj) -> 'ylist':
            res = ylist()
            if type(obj) in (list, ylist, tuple):
                for o in obj:
                    res += dfs_flatten(o)
            else:
                res.append(obj)
            return res
        return dfs_flatten(self)
    
    def collect(self, *target_type) -> 'ylist':
        res = ylist()
        for x in self:
            for t in target_type:
                try:
                    res.append(t(x))
                    break
                except:
                    pass
        return res
    
    def filter(self, *target_type) -> 'ylist':
        res = ylist()
        for x in self:
            if type(x) in target_type:
                res.append(x)
        return res

    @staticmethod
    def random(len, l, r) -> 'ylist':
        return ylist(random.randint(l, r) for _ in range(len))

    def to_dic(self) -> 'ydic':
        res = ydic()
        for i, x in enumerate(self):
            res[i] = x
        return res

    ##------------------------

    def trans(self) -> 'Trans':
        return Trans(self)

class Trans:

    def __init__(self, l: list) -> None:
        self.l = ylist(l)
        
    def finish(self) -> 'ylist':
        return self.l

    def do_mapping(self, mapper: dict) -> 'Trans':
        self.l = ylist(mapper[x] if x in mapper else x for x in self.l)
        return self

    def mapping__fibo(self, k0, k1, k2, reverse=False) -> 'Trans':
        def fibo_random(k0, k1, k2) -> 'ylist':
            pri = [
                32, 101, 114, 116, 115, 97, 110, 
                10, 105, 111, 102, 108, 95, 112, 
                100, 39, 99, 40, 41, 61, 46, 
                117, 109, 58, 119, 44, 91, 93, 
                98, 121, 118, 103, 49, 104, 45, 
                62, 123, 48, 125, 34, 43, 47,
            ]
            res = []
            cnt = 0
            while len(res) < k0:
                cnt += 1
                cur = (k1+k2) % k0
                if cur not in res and cnt >= 12:
                    res.append(cur)
                k1, k2 = k2, cur
            res = [x for x in res if x < 256]
            pr_cnt = len(pri)
            pr = [x for x in res if x >= 1 and x <= pr_cnt]
            def force_mapping(a, b):
                tmp = res[a]
                pos_b = res.index(b)
                res[a] = b
                res[pos_b] = tmp
            force_mapping_list = [(0, 0), (255, 255)]
            for i in range(pr_cnt):
                force_mapping_list.append((pri[i], pr[i]))
            for a, b in force_mapping_list:
                force_mapping(a, b)
            if len(res) != 256:
                raise
            for i in range(256):
                if i not in res:
                    raise
            return ylist(res)
        mapper = fibo_random(k0, k1, k2).to_dic()
        if reverse:
            mapper = mapper.reverse()
        return self.do_mapping(mapper)

#------------------------   

class ydic(dict):

    def gevert(self, key, convert_type=None, default=None):
        ret = self.get(key, default)
        if convert_type != None:
            try:
                return convert_type(ret)
            except:
                return default
        return ret            

    def reverse(self, join=False) -> 'ydic':
        res = ydic()
        for k, v in self.items():
            if v not in res:
                res[v] = k
                continue
            if not join:
                raise
            if type(res[v]) == ylist:
                res[v].append(k)
            else:
                res[v] = ylist([res[v], k])
        return res

#------------------------

class ypic():

    def __init__(self, p: Image.Image) -> None:
        self.p = p

    @staticmethod
    def open(path: str) -> 'ypic':
        return ypic(Image.open(path))
    
    def resize(self, width: int, height: int) -> 'ypic':
        if width == None and height == None:
            return self
        w, h = self.p.size
        if width == None:
            width = w * height // h
        if height == None:
            height = h * width // w
        self.p = self.p.resize((width, height), Image.Resampling.LANCZOS)
        return self
    
    def to_bytes(self, format='png', quality=None) -> bytes:
        buffer = BytesIO()
        self.p.save(buffer, format=format, quality=quality)
        b = buffer.getvalue()
        buffer.close()
        return b

    @staticmethod
    def empty_pic(w: int, h: int) -> 'ypic':
        return ypic(Image.new('RGB', (w, h)))

    @staticmethod
    def from_file(path: str) -> 'ypic':
        return ypic(Image.open(path).convert('RGB'))
    
    def to_file(self, path: str = None) -> 'ypic':
        if path == None:
            path = f'{ystr().timestamp().now()}.png'
        self.p.save(path)
    
    def set_pixel(self, pos: tuple[int, int], value: int, chn: int) -> 'ypic':
        data = list(self.p.getpixel(pos))
        data[chn] = value
        self.p.putpixel(pos, tuple(data))
        return self
    
    # pp: (pos, channel, value)
    def load_pps(self, pp_list: list[tuple[int, int, int]]) -> 'ypic':
        if len(pp_list) == 0:
            return self
        w, h = self.p.size
        pp_need = pp_list[-1][0] + 1
        print(f'image size = {w}x{h}, pp count = {w*h}, pp need = {pp_need} ({(pp_need)/(w*h)*100}%)')
        if w*h < pp_need:
            raise Exception(f'image too small, which pp count = {w*h} but need {pp_need}')
        for p, t, d in pp_list:
            x = p % w
            y = p // w
            self.set_pixel((x, y), d, t)
        return self
    
    def load_str(self, s: str, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ypic':
        def gen_pixel_point(data: list) -> list:
            if data == None or len(data) == 0:
                return []
            res = [(0, 0, 0)]
            for i, d in enumerate(data):
                nxt_p, nxt_t = ypic.__get_next__(res[i], shift)
                res.append((nxt_p, nxt_t, d))
            return res[1:]
        data = ylist.from_str(s)
        str__len = ystr(len(data))
        if len(str__len) > head_len:
            raise Exception(f'head len too long which reach {len(str__len)}')
        data = ylist(int(x) for x in str__len.number().format(head_len)) + data
        if k0 != None:
            data = data.trans().mapping__fibo(k0, k1, k2).finish()
        self.load_pps(gen_pixel_point(data))
        return self
    
    def load_bytes(self, b: bytes, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ypic':
        def gen_pixel_point(data: list) -> list:
            if data == None or len(data) == 0:
                return []
            res = [(0, 0, 0)]
            for i, d in enumerate(data):
                nxt_p, nxt_t = ypic.__get_next__(res[i], shift)
                res.append((nxt_p, nxt_t, d))
            return res[1:]
        data = ylist.from_bytes(b)
        str__len = ystr(len(data))
        if len(str__len) > head_len:
            raise Exception(f'head len too long which reach {len(str__len)}')
        data = ylist(int(x) for x in str__len.number().format(head_len)) + data
        if k0 != None:
            data = data.trans().mapping__fibo(k0, k1, k2).finish()
        self.load_pps(gen_pixel_point(data))
        return self
    
    def fetch_str(self, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ystr':
        pp_data = list(self.p.getdata())
        pps = [(0, 0, 0)]
        while True:
            nxt_p, nxt_t = ypic.__get_next__(pps[-1], shift)
            if nxt_p >= len(pp_data):
                break
            pps.append((nxt_p, nxt_t, pp_data[nxt_p][nxt_t]))
        data = ylist(pp[2] for pp in pps[1:])
        if k0 != None:
            data = data.trans().mapping__fibo(k0, k1, k2, reverse=True).finish()
        body_len = int(ystr().join(ystr(x) for x in data[:head_len]))
        data = data[head_len:head_len+body_len]
        return ylist(data).to_str()
    
    def fetch_bytes(self, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ybytes':
        pp_data = list(self.p.getdata())
        pps = [(0, 0, 0)]
        while True:
            nxt_p, nxt_t = ypic.__get_next__(pps[-1], shift)
            if nxt_p >= len(pp_data):
                break
            pps.append((nxt_p, nxt_t, pp_data[nxt_p][nxt_t]))
        data = ylist(pp[2] for pp in pps[1:])
        if k0 != None:
            data = data.trans().mapping__fibo(k0, k1, k2, reverse=True).finish()
        body_len = int(ystr().join(ystr(x) for x in data[:head_len]))
        data = data[head_len:head_len+body_len]
        return ylist(data).to_bytes()
    
    def load_files(self, *filepath: str, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ypic':
        all_content = {
            'files': []
        }
        all_content_len = 0
        for f in filepath:
            content = ystr().from_file(f)
            all_content['files'].append({
                'content': content,
                'filepath': f,
                'md5': content.md5(),
            })
            all_content_len += len(content)
        all_content['md5'] = ystr().json().from_object(all_content['files']).md5()
        self.load_str(
            ystr().json().from_object(all_content),
            k0 = k0,
            k1 = k1,
            k2 = k2,
            shift = shift,
            head_len = head_len,
        )
        print(f'load {all_content_len} chars')
        return self

    def fetch_files(self, res_dic: str, k0=None, k1=None, k2=None, shift=100, head_len=10) -> 'ypic':
        all_content = ystr(self.fetch_str(
            k0 = k0,
            k1 = k1,
            k2 = k2,
            shift = shift,
            head_len = head_len,
        )).json().to_dic()
        if all_content['md5'] != ystr().json().from_object(all_content['files']).md5():
            print('warn - md5 check not ok: overall')
        print('fetching files:')
        for i, f in enumerate(all_content['files']):
            content = ystr(f['content'])
            file_path = f['filepath']
            if f['md5'] != content.md5():
                print(f'warn - md5 check not ok: {file_path}')
            else:
                print(f'    {i+1}.{file_path} ({len(content)} chars)')
            content.to_file(os.path.join(res_dic, file_path), force=True)
        return self

    def __get_next__(pp: tuple, shift) -> tuple:    
        p, c, d = pp
        shift = c + d%9 + 1 + shift
        p += shift // 3
        c = shift % 3
        return p, c
    

    