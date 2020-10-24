# 自定义请求钩子, 相当于中间件

from flask import request, g
from common.utils.jwt_utils import verify_token


def get_user_id():
    """获取用户的user_id"""

    # 获取请求头中的token
    token = request.headers.get('Authorization')

    g.user_id = None  # 如果未登录, userid=None

    if token:  # 如果传递了token
        # 校验token
        data = verify_token(token)

        if data:  # 校验成功
            g.user_id = data.get('user_id')  # 是从登录接口里面写入的key,所以获取的key为user_id












