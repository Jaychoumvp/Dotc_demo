from flask import Flask
from common.settings.config import config_dict
from common.utils.constants import EXTRA_ENV_CONFIG
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
import importlib
from common.utils.converters import MobileConverter
from flask_migrate import Migrate

# 全局 db
db = SQLAlchemy()
# 全局 redis_client
redis_client = None


def register_converters(app):
    """注册自定义路由转化器"""
    app.url_map.converters['mob'] = MobileConverter


def register_bp(app: Flask):
    """注册蓝图"""
    # 进行局部导入, 避免组件没有初始化完成
    # 由于在代码体中不推荐使用 import app.resources.user as user
    # 所有我们使用 python 内部的导包函数来导入模块
    user = importlib.import_module('app.resources.user')
    app.register_blueprint(user.blueprint)


def register_extensions(app):
    """第三方组件初始化"""

    # 数据库初始化
    db.init_app(app)

    # redis 初始化
    global redis_client
    # 设置 decode_responses=True redis 获取到数据后会自动调用 decode 解码数据
    redis_host = app.config['REDIS_HOST']
    redis_port = app.config['REDIS_PORT']
    redis_client = StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    Migrate(app, db)
    # 导入模型所在的模块
    importlib.import_module('common.models.user')


def create_flask_app(type):
    """创建flask应用"""

    # 创建flask应用
    app = Flask(__name__)

    # 根据类型加载配置子类
    config_class = config_dict[type]
    # 先加载默认配置
    app.config.from_object(config_class)
    # 再加载额外配置
    app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)

    # 返回应用
    return app


def create_app(type):
    """创建应用 和 组件初始化"""

    # 创建flask应用
    app = create_flask_app(type)

    # 注册路由转换器
    register_converters(app)

    # 组件初始化
    register_extensions(app)

    # 注册蓝图
    register_bp(app)

    return app

