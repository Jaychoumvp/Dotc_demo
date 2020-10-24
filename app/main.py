from app import create_app

# 创建web应用
app = create_app('dev')


@app.route('/')
def route_map():
    """定义根路由: 获取所有路由规则"""

    return {rule.endpoint: rule.rule for rule in app.url_map.iter_rules()}

