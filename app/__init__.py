from flask import Flask
from common.settings.config import config_dict
from common.utils.constants import EXTRA_ENV_CONFIG


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
    # 组件初始化

    return app