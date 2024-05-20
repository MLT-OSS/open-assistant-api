from fastapi import APIRouter
from app.api.v1 import assistant, assistant_file, thread, message, files, runs, token, action

api_router = APIRouter(prefix="/v1")


def router_init():
    api_router.include_router(assistant.router, prefix="/assistants", tags=["assistants"])
    api_router.include_router(assistant_file.router, prefix="/assistants", tags=["assistants"])
    api_router.include_router(thread.router, prefix="/threads", tags=["threads"])
    api_router.include_router(message.router, prefix="/threads", tags=["messages"])
    api_router.include_router(runs.router, prefix="/threads", tags=["runs"])
    api_router.include_router(files.router, prefix="/files", tags=["files"])
    api_router.include_router(token.router, prefix="/tokens", tags=["tokens"])
    api_router.include_router(action.router, prefix="/actions", tags=["actions"])
