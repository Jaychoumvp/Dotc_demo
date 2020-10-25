from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, Text, String, JSON, DateTime

from app import db


class Channel(db.Model):
    """
    新闻频道
    """
    __tablename__ = 'news_channel'

    id = Column(Integer, primary_key=True, doc='频道ID')
    name = Column(String(30), doc='频道名称')
    is_default = Column(Boolean, default=False, doc='是否默认')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class UserChannel(db.Model):
    """
    用户关注频道表
    """
    __tablename__ = 'news_user_channel'

    id = Column(Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, doc='用户ID')
    channel_id = Column(Integer, doc='频道ID')
    sequence = Column(Integer, default=0, doc='序号')
    is_deleted = Column(Boolean, default=False, doc='是否删除')


class Article(db.Model):
    """
    文章基本信息表
    """
    __tablename__ = 'news_article_basic'

    class STATUS:
        DRAFT = 0  # 草稿
        UNREVIEWED = 1  # 待审核
        APPROVED = 2  # 审核通过
        FAILED = 3  # 审核失败
        DELETED = 4  # 已删除
        BANNED = 5  # 封禁

    id = Column(Integer, primary_key=True,  doc='文章ID')
    user_id = Column(Integer, doc='用户ID')
    channel_id = Column(Integer, doc='频道ID')
    title = Column(String(130), doc='标题')
    cover = Column(JSON, doc='封面')
    ctime = Column(DateTime, default=datetime.now, doc='创建时间')
    status = Column(Integer, default=0, doc='帖文状态')
    comment_count = Column(Integer, default=0, doc='评论数')


class ArticleContent(db.Model):
    """
    文章内容表
    """
    __tablename__ = 'news_article_content'

    article_id = Column(Integer, primary_key=True, doc='文章ID')
    content = Column(Text, doc='帖文内容')


class Attitude(db.Model):
    """
    文章态度表
    """
    __tablename__ = 'news_attitude'

    class ATTITUDE:
        DISLIKE = 0  # 不喜欢
        LIKING = 1  # 喜欢
        DELETE = -1  # 无态度

    id = Column(Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, doc='用户ID')
    article_id = Column(Integer, doc='文章ID')
    attitude = Column(Integer, doc='态度')


class Collection(db.Model):
    """
    用户收藏表
    """
    __tablename__ = 'news_collection'

    id = Column(Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, doc='用户ID')
    article_id = Column(Integer, doc='文章ID')
    is_deleted = Column(Boolean, default=False, doc='是否删除')


class Comment(db.Model):
    """
    文章评论
    """
    __tablename__ = 'news_comment'

    id = Column(Integer, primary_key=True, doc='评论ID')
    user_id = Column(Integer, doc='用户ID')
    article_id = Column(Integer, doc='文章ID')
    parent_id = Column(Integer, doc='被评论的评论id')
    reply_count = Column(Integer, default=0, doc='回复数')
    ctime = Column(DateTime, default=datetime.now, doc='创建时间')
    like_count = Column(Integer, default=0, doc='点赞数')
    content = Column(String(200), doc='评论内容')
