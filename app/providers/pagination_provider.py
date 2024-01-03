from fastapi_pagination import add_pagination


def register(app):
    add_pagination(app)
