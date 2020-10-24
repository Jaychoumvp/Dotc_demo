from datetime import datetime
from flask import current_app
from flask_restful import Resource
import random
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import regex
from sqlalchemy.orm import load_only
from app import redis_client, db
from common.models.user import User
from common.utils.constants import SMS_CODE_EXPIRE
from common.utils.jwt_utils import generate_token
from common.utils.parser import parse_mobile


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


class LoginResource(Resource):
    """注册登录"""

    def post(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('mobile', required=True, location='json', type=parse_mobile)
        parser.add_argument('code', required=True, location='json', type=regex(r'^\d{6}$'))
        args = parser.parse_args()
        mobile = args.mobile
        code = args.code

        # 校验短信验证码
        key = f'app:code:{mobile}'
        real_code = redis_client.get(key)

        if not real_code or real_code != code:
            return {'message': 'Invalid Code', 'data': None}, 400

        # 删除验证码
        redis_client.delete(key)

        # 校验成功, 查询数据库
        user = User.query.filter(User.mobile == mobile).first()

        if not user:  # 没有就创建用户
            user = User(mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)

        else:  # 有就更新登录时间
            user.last_login = datetime.now()

        db.session.commit()

        # 生成jwt
        token = generate_token({'userid': user.id})
        # 返回结果
        return {'token': token}, 201