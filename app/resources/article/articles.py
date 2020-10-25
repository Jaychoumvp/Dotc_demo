from datetime import datetime
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app import db
from common.models.article import Article
from common.models.user import User
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