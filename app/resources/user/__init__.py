from flask import Blueprint
from flask_restful import Api
from common.utils.constants import BASE_URL_PRIFIX
from .passport import SMSCodeResource
from common.utils.output import output_json

# 创建蓝图对象
blueprint = Blueprint('user', __name__, url_prefix=BASE_URL_PRIFIX)

# 创建Api对象
api = Api(blueprint)

# 绑定output, 响应数据输出格式为json
api.representation('application/json')(output_json)

# 添加类视图
api.add_resource(SMSCodeResource, '/sms/codes')