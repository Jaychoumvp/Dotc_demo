class DefaultConfig:
    """默认配置"""

    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/dotc'  # 连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的SQL

    # redis配置
    REDIS_HOST = 'localhost'  # ip
    REDIS_PORT = 6379  # 端口


config_dict = {
    'dev': DefaultConfig
}

