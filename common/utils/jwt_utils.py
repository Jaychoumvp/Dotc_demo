# 定义生成token的函数
# 定义检验token的函数



from datetime import datetime, timedelta

import jwt
from flask import current_app


def generate_token(payload):
    """
    生成jwt
    :param payload: dict 载荷
    :return: jwt
    """

    # 设置过期时间
    expiry = datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS'])
    secret = current_app.config['JWT_SECRET']
    algorithm = current_app.config['JWT_ALGORITHM']

    _payload = {'exp': expiry}
    _payload.update(payload)

    token = jwt.encode(_payload, secret, algorithm=algorithm)
    return token.decode()


def verify_token(token):
    """
    检验jwt
    :param token: jwt-token
    :return: dict: payload
    """

    secret = current_app.config['JWT_SECRET']
    algorithm = current_app.config['JWT_ALGORITHM']
    try:
        payload = jwt.decode(token, secret, algorithm=algorithm)
    except jwt.PyJWTError:
        payload = None

    return payload

