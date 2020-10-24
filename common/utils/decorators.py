#  定义装饰器


from functools import wraps
from flask import g


def login_required(f):
    """判断用户是否登录而执行被装饰器的接口"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user_id:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid Token', 'data': None}, 401

    return wrapper
