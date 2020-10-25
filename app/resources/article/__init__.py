from flask import Blueprint
from flask_restful import Api

from app.resources.article.articles import ArticleListResource
from app.resources.article.channel import AllChannelResource
from common.utils.constants import BASE_URL_PRIFIX
from common.utils.output import output_json


# 1.创建蓝图对象
blueprint = Blueprint('article', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
api = Api(blueprint)

# 绑定output, 响应数据输出格式为json
api.representation('application/json')(output_json)

# 添加类视图,绑定路由
api.add_resource(AllChannelResource, '/channels')
api.add_resource(ArticleListResource, '/articles')