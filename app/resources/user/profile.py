from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only
from common.models.user import User
from common.utils.decorators import login_required


class CurrentUserResource(Resource):
    """个人中心信息显示"""

    # 调用装饰器判断是否登录
    method_decorators = {'get': [login_required]}

    def get(self):
        # 获取用户id
        user_id = g.user_id
        # 只读取部分字段数据
        load_only_fields = [
            User.id,
            User.name,
            User.profile_photo,
            User.introduction,
            User.article_count,
            User.following_count,
            User.fans_count
        ]

        # 查询用户数据
        user = User.query.options(load_only(*load_only_fields)).filter(User.id == user_id).first()

        return user.to_dict()