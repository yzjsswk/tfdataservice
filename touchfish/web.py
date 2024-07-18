from .service import Service, logger
from .definition import *
from yfunc import *
from flask import Flask, request, Response, make_response
import time

def control(func):
    def handle_input(func):
        input = {}
        lack_para = []
        dup_para = []
        import inspect
        func_paras = inspect.signature(func).parameters
        for func_para in func_paras:
            if func_para in request.args:
                if func_para not in input:
                    input[func_para] = request.args[func_para]
                else:
                    dup_para.append(func_para)
            if func_para in request.form:
                if func_para not in input:
                    input[func_para] = request.form[func_para]
                else:
                    dup_para.append(func_para)
            if func_para in request.files:
                if func_para not in input:
                    input[func_para] = ybytes(request.files[func_para].read())
                else:
                    dup_para.append(func_para)
            if func_para not in input and func_paras[func_para].default is inspect.Parameter.empty:
                lack_para.append(func_para)
        return input, lack_para, dup_para
    def handle_output(data, time_cost, status=200) -> Response:
        if data == None:
            return make_response('')
        if isinstance(data, dict):
            res = {}
            res['time_cost'] = time_cost
            res['code'] = data.get('code', 'SSCTWF')
            res['status'] = data.get('status', 'success')
            res['msg'] = data.get('msg', 'ok')
            if 'code' in data:
                del data['code']
            if 'msg' in data:
                del data['msg']
            if 'status' in data:
                del data['status']
            if data == None or len(data) > 0:
                res['data'] = data
            res = ystr().json().from_object(res)
            return Response(res, status=status, content_type='application/json')
        if isinstance(data, bytes):
            res = make_response(data)
            # todo: file name
            res.headers['Content-Disposition'] = f'attachment; filename=fishdata'
            res.headers['Content-Type'] = 'application/octet-stream'
            return res
        if isinstance(data, str):
            return make_response(data)    
        logger.warning(f'unhandled response type: {type(data)}')
        return make_response(data)
    def wrap_func(*args, **kwargs):
        if len(args) > 0 or len(kwargs) > 0:
            logger.warning(f'warp func ignore para: args={args}, kwargs={kwargs}')
        request_id = ystr.uuid()
        logger.info(f"request start: request_id={request_id}, url={request.base_url}")
        t1 = int(time.time()*1000)
        # execute
        try:
            input, lack_para, dup_para = handle_input(func)
            if len(lack_para) > 0:
                res = get_dict_resp(RespStatus.fail, f'parameters required: {lack_para}', 'CTWF')
            elif len(dup_para) > 0:
                res = get_dict_resp(RespStatus.fail, f'parameters duplicated: {dup_para}', 'CTWF')
            else:
                res = func(**input)
        except Exception as e:
            e.add_note(f'Note: url = {request.base_url}')
            logger.exception(e)
            res = {'code':-999, 'status': 'fail', 'msg': str(e)}
        t2 = int(time.time()*1000)
        # make response
        try:
            resp = handle_output(res, t2-t1)    
        except Exception as e:
            e.add_note(f'Note: url = {request.base_url}')
            logger.exception(e)
            res = {'code':-998, 'status': 'fail', 'msg': str(e)}
        t3 = int(time.time()*1000)
        # record request log
        try:
            Service.add_request_log(
                request_id=request_id, url=request.base_url, time_cost=f'{t3-t1}+:{t2-t1},{t3-t2}',
                origin_input = {
                    'request.args': request.args,
                    'request.form': request.form,
                    'request.files': request.files,
                },
                real_input = input, 
                response = {
                    'code': resp.status_code,
                    'content_type': resp.content_type,
                    'content_length': f'{resp.content_length}({ybytes(resp.data).size()})',
                    'preview': ybytes(resp.data).desc()[:1000],
                },
                extra_info = '',
            )
        except Exception as e:
            e.add_note(f'Note: url = {request.base_url}')
            logger.exception(e)
            res = {'code':-997, 'status': 'fail', 'msg': str(e)}
        t4 = int(time.time()*1000)
        # update time cost of request log (including time cost of recording log)
        try:
            Service.update_request_time(request_id, {
                'total': t4-t1,
                'execute': t2-t1,
                'make_response': t3-t2,
                'record_log': t4-t3,            
            })
        except Exception as e:
            e.add_note(f'Note: url = {request.base_url}')
            logger.exception(e)
            res = {'code':-996, 'status': 'fail', 'msg': str(e)}
        logger.info(f"request end: request_id={request_id}, url={request.base_url}, time_cost={t4-t1}, input={input}, output={resp}")
        return resp
    wrap_func.__name__ = f'wrap__{func.__name__}'
    return wrap_func

tfwebserver = Flask(__name__)

@tfwebserver.route('/', methods=['GET'])
@control
def hello() -> str:
    return ystr().timestamp().now()

@tfwebserver.route('/stats', methods=['GET'])
@control
def stats() -> dict:
    return Service.statistic()
    
@tfwebserver.route('/fish/search', methods=['GET'])
@control
def search_fish (
            fuzzys: str = None, 
            value: str = None, 
            description: str = None, 
            identity: str = None,
            type: str = None, 
            tags: str = None, 
            is_marked: str = None,
            is_locked: str = None,
            page_num: str = None,
            page_size: str = None,
            with_preview: str = None,
    ) -> dict:
    if identity != None:
        identity = identity.split(',')
    if type != None:
        type = ylist(FishType.from_name(t) for t in type.split(',')).filter(FishType)
    tags = str_parse_tags(tags)
    if is_marked != None:
        if ystr(is_marked).of('true', '1'):
            is_marked = True
        elif ystr(is_marked).of('false', '0'):
            is_marked = False
        else:
            is_marked = None
    if is_locked != None:
        if ystr(is_locked).of('true', '1'):
            is_locked = True
        elif ystr(is_locked).of('false', '0'):
            is_locked = False
        else:
            is_locked = None
    if with_preview != None and ystr(with_preview).of('false', '0'):
            with_preview = False
    else:
        with_preview = True
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    try:
        page_size = int(page_size)
    except:
        page_size = 10
    if page_num < 1:
        page_num = 1
    if page_size < 1:
        page_size = 10
    total_count, fish = Service.search_fish(
        fuzzys=fuzzys, value=value, description=description, identity=identity,
        type=type, tags=tags, is_marked=is_marked, is_locked=is_locked,
        page_num=page_num, page_size=page_size, with_preview = with_preview,
    )
    total_page = total_count//page_size if total_count % page_size == 0 else total_count//page_size+1
    return {
        'page_num': page_num,
        'page_size': page_size,
        'total_page': total_page,
        'total_count': total_count,
        'fish': fish,
    }

@tfwebserver.route('/fish/add', methods=['POST'])
@control
def add_fish (
        value: bytes,
        type: str,
        description: str = None,
        tags: str = None,
        is_marked: str = None,
        is_locked: str = None,
        extra_info: str = None,
    ) -> dict:
    if type != None:
        type = FishType.from_name(type)
    if is_marked != None and ystr(is_marked).of('true', '1'):
        is_marked = True
    else:
        is_marked = False
    if is_locked != None and ystr(is_locked).of('true', '1'):
        is_locked = True
    else:
        is_locked = False
    tags = str_parse_tags(tags)
    return Service.add_fish(
        value=value, description=description, type=type, 
        tags=tags, is_marked=is_marked, is_locked=is_locked,
        extra_info=extra_info,
    )

@tfwebserver.route('/fish/modify', methods=['POST'])
@control
def modify_fish (
        identity: str, 
        description: str = None,
        tags: str = None,
        extra_info: str = None,
    ) -> dict:
    tags = str_parse_tags(tags)
    return Service.modify_fish(
        identity=identity, description=description,
        tags=tags, extra_info=extra_info,
    )
    
@tfwebserver.route('/fish/pin', methods=['POST'])
@control
def pin_fish(identity: str) -> dict:
    return Service.pin_fish(identity)

@tfwebserver.route('/fish/remove', methods=['POST'])
@control
def remove_fish(identity: str) -> dict:
    return Service.remove_fish(identity)

@tfwebserver.route('/fish/lock', methods=['POST'])
@control
def lock_fish(identity: str) -> dict:
    return Service.lock_fish(identity)

@tfwebserver.route('/fish/unlock', methods=['POST'])
@control
def unlock_fish(identity: str) -> dict:
    return Service.unlock_fish(identity)

@tfwebserver.route('/fish/mark', methods=['POST'])
@control
def mark_fish(identity: str) -> dict:
    return Service.mark_fish(identity)

@tfwebserver.route('/fish/unmark', methods=['POST'])
@control
def unmark_fish(identity: str) -> dict:
    return Service.unmark_fish(identity)

@tfwebserver.route('/fish/clear', methods=['POST'])
@control
def clear_fish(second_delta: str) -> dict:
    # todo: req/resp handle and error handle
    second_delta = int(second_delta)
    identity__cleared_fish = Service.clear_fish(second_delta=second_delta)
    return {
        'cleared_identitys': identity__cleared_fish
    }

@tfwebserver.route('/resource/fetch', methods=['GET'])
@control
def fetch_resource(identity: str) -> bytes:
    return Service.fetch_resource(identity)

@tfwebserver.route('/resource/preview', methods=['GET'])
@control
def fetch_preview(identity: str) -> bytes:
    return Service.fetch_preview(identity)

