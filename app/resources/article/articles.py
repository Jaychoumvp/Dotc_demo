from datetime import datetime

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from common.models.article import Article, ArticleContent, Collection, Attitude
from common.models.user import User, Relation
from common.utils.constants import HOME_PRE_PAGE


class ArticleListResource(Resource):
    """首页文章列表展示"""

    def get(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('channel_id', required=True, location='args', type=int)
        parser.add_argument('timestamp', required=True, location='args', type=int)
        args = parser.parse_args()
        channel_id = args.channel_id
        timestamp = args.timestamp

        # 如果为"推荐"频道, 先返回空数据
        if channel_id == 0:
            return {'results': [], 'pre_timestamp': 0}

        # 将timestamp转为datetime类型
        date = datetime.fromtimestamp(timestamp * 0.001)

        # 查询频道中对应的数据  连接查询    要求: 频道对应 & 审核通过 & 发布时间 < timestamp
        load_fields = [Article.id,
                       Article.title,
                       Article.user_id,
                       Article.ctime,
                       User.name,
                       Article.comment_count,
                       Article.cover]
        data = db.session.query(*load_fields).join(User, Article.user_id == User.id).\
            filter(Article.channel_id == channel_id, Article.status == Article.STATUS.APPROVED, Article.ctime < date)\
            .order_by(Article.ctime).limit(HOME_PRE_PAGE).all()

        # 序列化
        articles = [
            {
                'art_id': item.id,
                'title': item.title,
                'aut_id': item.user_id,
                'pubdate': item.ctime.isoformat(),
                'aut_name': item.name,
                'comm_count': item.comment_count,
                'cover': item.cover
            }
            for item in data]

        # 设置该组数据最后一条的发布时间 为pre_timestamp
        # 日期对象 转为 时间戳   日期对象.timestamp()
        pre_timestamp = int(data[-1].ctime.timestamp() * 1000) if data else 0

        # 返回数据
        return {'results': articles, 'pre_timestamp': pre_timestamp}


class ArticleDetailResource(Resource):
    """文章详情+用户对文章的态度与收藏状态"""

    def get(self, article_id):
        # 查询基础数据
        load_fields = [Article.id,
                       Article.title,
                       Article.ctime,
                       Article.user_id,
                       User.name,
                       User.profile_photo,
                       ArticleContent.content]
        data = db.session.query(*load_fields). \
            join(User, Article.user_id == User.id). \
            join(ArticleContent, Article.id == ArticleContent.article_id). \
            filter(Article.id == article_id).first()

        # 序列化
        article_dict = {
            'art_id': data.id,
            'title': data.title,
            'pubdate': data.ctime.isoformat(),
            'aut_id': data.user_id,
            'aut_name': data.name,
            'aut_photo': data.profile_photo,
            'content': data.content,
            'is_followed': False,
            'attitude': -1,
            'is_collected': False
        }

        # 获取参数
        user_id = g.user_id

        # 判断用户是否已登录
        if user_id:
            # 查询用户的关注关系   用户 -> 作者
            relation_obj = Relation.query.options(load_only(Relation.id)). \
                filter(Relation.user_id == user_id, Relation.author_id == data.user_id,
                       Relation.relation == Relation.RELATION.FOLLOW).first()

            article_dict['is_followed'] = True if relation_obj else False

            # 查询用户的收藏关系  用户 -> 文章    只查询主键即可
            collect_obj = Collection.query.options(load_only(Collection.id)). \
                filter(Collection.user_id == user_id, Collection.article_id == article_id,
                       Collection.is_deleted == False).first()

            article_dict['is_collected'] = True if collect_obj else False

            # 查询用户的文章态度  用户 -> 文章
            atti_obj = Attitude.query.options(load_only(Attitude.attitude)). \
                filter(Attitude.user_id == user_id, Attitude.article_id == article_id).first()

            if not atti_obj:  # 如果不存在关系, 直接设置无态度
                attitude = -1
            else:
                attitude = atti_obj.attitude

            article_dict['attitude'] = attitude

        # 返回数据
        return article_dict