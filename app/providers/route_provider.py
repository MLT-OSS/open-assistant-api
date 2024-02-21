import logging

from app.api.routes import api_router, router_init
from config.config import settings


def boot(app):
    # 注册api路由[app/api/routes.py]
    router_init()
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # 打印路由
    if app.debug:
        for route in app.routes:
            logging.info({"path": route.path, "name": route.name, "methods": route.methods})
