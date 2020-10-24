from datetime import datetime
from app import db
from sqlalchemy import Column, String, Integer, DateTime


class User(db.Model):
    """用户基本信息"""

    __tablename__ = 'user_basic'

    id = Column(Integer, primary_key=True, doc='用户ID')
    mobile = Column(String(11), doc='手机号')
    name = Column(String(20), doc='昵称')
    last_login = Column(DateTime, doc='最后登录时间')
    introduction = Column(String(50), doc='简介')
    article_count = Column(Integer, default=0, doc='作品数')
    following_count = Column(Integer, default=0, doc='关注的人数')
    fans_count = Column(Integer, default=0, doc='粉丝数')
    profile_photo = Column(String(130), doc='头像')

    def to_dict(self):
        """模型转字典, 用于序列化处理"""

        return {
            'id': self.id,
            'name': self.name,
            'photo': self.profile_photo,
            'intro': self.introduction,
            'art_count': self.article_count,
            'follow_count': self.following_count,
            'fans_count': self.fans_count
        }


class Relation(db.Model):
    """用户关系表"""

    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = Column(Integer, primary_key=True, doc='主键ID')
    user_id = Column(Integer, doc='用户ID')
    author_id = Column(Integer, doc='目标用户ID')
    relation = Column(Integer, doc='关系')
    update_time = Column(DateTime, default=datetime.now, doc='更新时间')