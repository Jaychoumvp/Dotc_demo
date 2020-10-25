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
    method_decorators = {'post': [login_required], 'get': [login_required]}

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

    def get(self):
        """获取关注列表"""
        # 获取参数
        user_id = g.user_id
        parser = RequestParser()
        parser.add_argument('page', default=1, location='args', type=int)
        parser.add_argument('per_page', default=2, location='args', type=int)
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page

        # 查询数据 当前用户的关注列表
        pn = User.query.options(load_only(User.id, User.name, User.profile_photo, User.fans_count)). \
            join(Relation, User.id == Relation.author_id). \
            filter(Relation.user_id == user_id, Relation.relation == Relation.RELATION.FOLLOW). \
            order_by(Relation.update_time). \
            paginate(page, per_page)

        # 查询当前用户的粉丝列表
        fans_list = Relation.query.options(load_only(Relation.user_id)). \
            filter(Relation.author_id == user_id, Relation.relation == Relation.RELATION.FOLLOW).all()

        # 序列化
        author_list = []
        for item in pn.items:
            author_dict = {
                'id': item.id,
                'name': item.name,
                'photo': item.profile_photo,
                'fans_count': item.fans_count,
                'mutual_follow': False
            }

            # 如果该作者也关注了当前用户, 则为互相关注
            for fans in fans_list:
                if item.id == fans.user_id:
                    author_dict['mutual_follow'] = True
                    break

            author_list.append(author_dict)

        # 返回数据
        return {'results': author_list, 'per_page': per_page, 'page': pn.page, 'total_count': pn.total}






class UnFollowUserResource(Resource):
    """取消关注用户"""
    method_decorators = {'delete': [login_required]}

    def delete(self, target):
        # 获取参数
        user_id = g.user_id

        # 更新用户关系
        Relation.query.filter(Relation.user_id == user_id, Relation.author_id == target,
                              Relation.relation == Relation.RELATION.FOLLOW).update(
            {'relation': 0, 'update_time': datetime.now()})

        # 让作者的粉丝数量-1
        User.query.filter(User.id == target).update({'fans_count': User.fans_count - 1})
        # 让用户的关注数量-1
        User.query.filter(User.id == user_id).update({'following_count': User.following_count - 1})

        db.session.commit()
        return {'target': target}