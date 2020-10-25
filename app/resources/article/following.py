from datetime import datetime

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from common.models.user import Relation, User
from common.utils.decorators import login_required


class FollowUserResource(Resource):
    """关注用户"""
    method_decorators = {'post': [login_required]}

    def post(self):
        # 获取参数
        user_id = g.user_id
        parser = RequestParser()
        parser.add_argument('target', required=True, location='json', type=int)
        args = parser.parse_args()
        author_id = args.target

        # 查询数据
        relation = Relation.query.options(load_only(Relation.id)).filter(Relation.user_id == user_id,
                                                                         Relation.author_id == author_id).first()

        if relation:  # 如果有, 修改记录
            relation.relation = Relation.RELATION.FOLLOW
            relation.update_time = datetime.now()

        else:  # 如果没有, 新增记录
            relation = Relation(user_id=user_id, author_id=author_id, relation=Relation.RELATION.FOLLOW)
            db.session.add(relation)

        # 让作者的粉丝数量+1
        User.query.filter(User.id == author_id).update({'fans_count': User.fans_count + 1})
        # 让用户的关注数量+1
        User.query.filter(User.id == user_id).update({'following_count': User.following_count + 1})

        db.session.commit()

        # 返回结果
        return {'target': author_id}