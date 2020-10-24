from flask import current_app
from flask_restful import Resource
import random
from app import redis_client
from common.utils.constants import SMS_CODE_EXPIRE


class SMSCodeResource(Resource):
    """获取短信验证码"""

    def get(self, mobile):
        # 生成短信验证码
        code = f'{random.randint(0, 999999):06}'

        # 保存验证码(redis)  app:code:18912341234   123456
        key = f'app:code:{mobile}'
        redis_client.set(key, code, ex=SMS_CODE_EXPIRE)

        # 发送短信  第三方短信平台 celery
        print(f'短信验证码: "mobile": {mobile}, "code": {code}')

        # 返回结果，为了方便调试，在 debug 模式下将短信验证码返回给客户端
        if current_app.config['DEBUG']:
            return {'mobile': mobile, 'code': code}
        return {'mobile': mobile}