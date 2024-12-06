# JSON 数据提交通用方法

from django.http import JsonResponse

def success_api(msg: str = "成功"):
    """ 成功响应 默认值”成功“ """
    res = {
        'msg': msg,
        'success': True,
    }
    return JsonResponse(res, safe=False)


def fail_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    res = {
        'msg': msg,
        'success': False,
    }
    return JsonResponse(res, safe=False)


def table_api(msg: str = "success", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
    res = {
        'msg': msg,
        'code': 0,
        'data': data,
        'count': count,
        'limit': limit
    }
    return JsonResponse(res, safe=False,json_dumps_params={'ensure_ascii': False})

# 返回单页数据
def json_api(code=200,msg="success",data=None):
    # 包括200（成功）、201（创建）、400（错误请求）、401（未授权）、403（禁止）、404（未找到）、500（服务器错误）
    res={
        "code": code,
        "message": msg,
        "data": data
    }
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

# 返回多页数据
def json_list_api(code=200,msg="success",data=None,total=0,limit=10, page=1):
    res={
        "code": code,
        "message": msg,
        "data": {
            'total': total,
            'limit': limit,
            'page': page,
            'data': data
        }
    }
    return JsonResponse(res, safe=False,json_dumps_params={'ensure_ascii': False})

