from flask_restful import Resource


class SMSCodeResource(Resource):
    """获取短信验证码"""
    def get(self):
        return {'foo': 'get'}