from celery.signals import after_setup_logger

from app.providers import logging_provider

from app.providers.celery_app import celery_app  # noqa


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logging_provider.register()


if __name__ == '__main__':
    # 方便用代码启动调试
    cmd_argv = ["-A", "worker.celery_app", "worker", "-c", "1"]
    celery_app.start(argv=cmd_argv)
