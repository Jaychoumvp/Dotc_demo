from flask_restful import Resource
from sqlalchemy.orm import load_only
from common.models.article import Channel


class AllChannelResource(Resource):
    """所有频道"""

    def get(self):
        # 查询所有的频道
        channels = Channel.query.options(load_only(Channel.id, Channel.name)).all()

        # 序列化
        channel_list = [channel.to_dict() for channel in channels]

        # 返回数据
        return {'channels': channel_list}