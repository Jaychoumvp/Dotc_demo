from flask import g
from flask_restful import Resource
from flask_restful.inputs import regex
from flask_restful.reqparse import RequestParser

from app import db
from common.models.article import Comment, Article
from common.models.user import User
from common.utils.decorators import login_required


class CommentsResource(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        """发布评论"""

        # 获取参数
        user_id = g.user_id
        parser = RequestParser()
        parser.add_argument('target', required=True, location='json', type=int)
        parser.add_argument('content', required=True, location='json', type=regex(r'.+'))
        parser.add_argument('parent_id', location='json', type=int)
        args = parser.parse_args()
        target = args.target
        content = args.content
        parent_id = args.parent_id

        # 判断 生成 评论 还是 子评论
        if parent_id:  # 子评论

            # 生成子评论记录
            comment = Comment(user_id=user_id, article_id=target, content=content, parent_id=parent_id)
            db.session.add(comment)

            # 让评论的回复数量+1
            Comment.query.filter(Comment.id == parent_id).update({'reply_count': Comment.reply_count + 1})

        else:  # 评论

            # 生成评论记录
            comment = Comment(user_id=user_id, article_id=target, content=content, parent_id=0)
            db.session.add(comment)

            # 让文章的评论数量+1
            Article.query.filter(Article.id == target).update({'comment_count': Article.comment_count + 1})

        db.session.commit()

        # 返回结果
        return {'com_id': comment.id, 'target': target}

    def get(self):
        """获取评论列表"""

        # 获取参数
        parser = RequestParser()
        parser.add_argument('source', required=True, location='args', type=int)
        parser.add_argument('offset', default=0, location='args', type=int)
        parser.add_argument('limit', default=10, location='args', type=int)
        parser.add_argument('type', required=True, location='args', type=regex(r'[ac]'))
        args = parser.parse_args()
        source = args.source
        offset = args.offset
        limit = args.limit
        type = args.type

        # 判断获取 评论列表 or 回复列表
        if type == 'a':  # 评论列表

            # 查询文章的评论列表  需求: 分页
            comments = db.session.query(Comment.id, Comment.user_id, User.name, User.profile_photo, Comment.ctime, Comment.content, Comment.reply_count, Comment.like_count).\
                join(User, Comment.user_id == User.id).\
                filter(Comment.article_id == source, Comment.id > offset, Comment.parent_id == 0).\
                limit(limit).all()

            # 查询评论总数
            total_count = Comment.query.filter(Comment.article_id == source, Comment.parent_id == 0).count()

            # 指定文章的评论列表中最后一条评论的id
            end_comment = db.session.query(Comment.id).filter(Comment.article_id == source, Comment.parent_id == 0)\
                .order_by(Comment.id).first()

        else:  # 回复列表

            # 查询某条评论的回复列表
            comments = db.session.query(Comment.id,
                                        Comment.user_id,
                                        User.name,
                                        User.profile_photo,
                                        Comment.ctime,
                                        Comment.content,
                                        Comment.reply_count,
                                        Comment.like_count). \
                join(User, Comment.user_id == User.id). \
                filter(Comment.parent_id == source, Comment.id > offset). \
                limit(limit).all()

            # 查询某条评论的回复总数
            total_count = Comment.query.filter(Comment.parent_id == source).count()

            # 指定评论的回复列表中最后一条回复的id
            end_comment = db.session.query(Comment.id).filter(Comment.parent_id == source).order_by(
                Comment.id).first()


        # 序列化
        comment_list = [{
            "com_id": item.id,
            'aut_id': item.user_id,
            'aut_name': item.name,
            'aut_photo': item.profile_photo,
            'pubdate': item.ctime.isoformat(),
            'content': item.content,
            'reply_count': item.reply_count,
            'like_count': item.like_count
        } for item in comments]

        end_id = end_comment.id if end_comment else None

        # 获取本次请求最后一条数据的id
        last_id = comments[-1].id if comments else None

        # 返回数据
        return {'results': comment_list, 'total_count': total_count, 'last_id': last_id, 'end_id': end_id}