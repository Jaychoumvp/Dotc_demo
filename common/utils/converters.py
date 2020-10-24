# 自定义路由转化器


from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    """手机号格式"""
    regex = r'1[3-9]\d{9}'


